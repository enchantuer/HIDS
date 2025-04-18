import os
import pyshark
import requests
import hashlib
import json
import sys
from scapy.all import rdpcap, wrpcap, Raw
sys.path.append(os.path.abspath(".."))
from config import VT_API_KEY

# Configuration
cache_file = "vt_cache.json"


# Loading VirusTotal cache
if os.path.exists(cache_file):
    with open(cache_file, "r") as f:
        vt_cache = json.load(f)
else:
    vt_cache = {}


def vt_request(endpoint, value):
    """
    VirusTotal query with cache.
    :param endpoint: The ip, domain or payload of the pcap file.
    :param value: The value of the endpoint.
    :return: The data of the Virus Total request if it exist, else None.
    """
    if value in vt_cache:
        return vt_cache[value]
    headers = {"x-apikey": VT_API_KEY, "accept": "application/json"}
    response = requests.get(f"https://www.virustotal.com/api/v3/{endpoint}/{value}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        vt_cache[value] = data
        with open(cache_file, "w") as f:
            json.dump(vt_cache, f, indent=4)
        return data
    return None


def check_ip(ip):
    """
    Verification of IP adresses.
    :param ip: The Ip of the pcap file.
    :return: The statistique of malicious or suspicious if it exist, else False.
    """
    data = vt_request("ip_addresses", ip)
    if data:
        stats = data['data']['attributes']['last_analysis_stats']
        return stats['malicious'] > 0 or stats['suspicious'] > 0
    return False


def check_domain(domain):
    """
    Verification of domains.
    :param domain: The domain of the pcap file.
    :return: The statistique of malicious or suspicious if it exist, else False.
    """
    data = vt_request("domains", domain)
    if data:
        stats = data['data']['attributes']['last_analysis_stats']
        return stats['malicious'] > 0 or stats['suspicious'] > 0
    return False


def check_file_hash(payload):
    """
    Checking downloaded files.
    :param payload: Payload of the pcap file.
    :return: The statistique of malicious or suspicious if it exist, else False.
    """
    sha256_hash = hashlib.sha256(payload).hexdigest()
    data = vt_request("files", sha256_hash)
    if data:
        stats = data['data']['attributes']['last_analysis_stats']
        return stats['malicious'] > 0 or stats['suspicious'] > 0
    return False


def analyse_pcap_with_VT(pcap_path):
    """
    Scans a PCAP file with Virus Total and returns the detected alerts.
    :param pcap_path: Path of the PCAP file to be analyzed.
    :return: The alert name if an alert is detected, otherwise None.
    """
    packets = rdpcap(pcap_path)
    malicious_packets = []

    for pkt in packets:
        if pkt.haslayer(Raw):
            payload = bytes(pkt[Raw].load)
            file_malicious = check_file_hash(payload)
        else:
            file_malicious = False

        if pkt.haslayer("IP"):
            src_ip = pkt["IP"].src
            dst_ip = pkt["IP"].dst
            ip_malicious = check_ip(src_ip) or check_ip(dst_ip)
        else:
            ip_malicious = False

        if pkt.haslayer("DNS") and hasattr(pkt["DNS"], "qry_name"):
            domain = pkt["DNS"].qry_name.decode()
            domain_malicious = check_domain(domain)
        else:
            domain_malicious = False

        if file_malicious or ip_malicious or domain_malicious:
            if file_malicious:
                attack_name = "malicious_file"
            elif ip_malicious:
                attack_name = "malicious_IP"
            elif domain_malicious:
                attack_name = "malicious_domain"

            malicious_packets.append((pkt, attack_name))

    return attack_name


"""
alert = analyse_pcap_with_VT("../../Téléchargements/Extrait/ext_7.pcap")
print(alert)
"""