import os
import requests
import sys
from scapy.all import rdpcap, IP
import shutil
sys.path.append(os.path.abspath(".."))
from config import ABUSEIPDB_API_KEY


def check_ip_abuse(ip):
    """
    Check if IP address is malicious with the API of AbuseIPDB.
    :param ip: The ip of the pcap file.
    :return: True or False, if the ip is malicious or not.
    """
    url = f'https://api.abuseipdb.com/api/v2/check'
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    #Check in the last 90 days
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        #Check if the score is sup at 50
        if data['data']['abuseConfidenceScore'] > 50:
            return True
    return False


def analyse_pcap_with_abuseIPDB(pcap_file):
    """
    Scans a PCAP file with AbuseIPDB and returns the detected alert, malicious IP.
    :param pcap_file: Path of the PCAP file to be analyzed.
    :return: The alert name if an alert is detected, otherwise None.
    """
    packets = rdpcap(pcap_file)
    for packet in packets:
        #Check if the packet conains a IP layer 
        if packet.haslayer(IP):  
            ip_dest = packet[IP].dst
            if check_ip_abuse(ip_dest): 
                print(f"IP malveillante détectée: {ip_dest}")
                alert = "malicious_ip"
                return alert
                

alert= analyse_pcap_with_abuseIPDB("../../Téléchargements/Extrait/ext_10.pcap")
print(alert)
