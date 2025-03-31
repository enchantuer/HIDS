import os
import requests
import sys
from scapy.all import rdpcap, IP
import shutil
sys.path.append(os.path.abspath(".."))
from config import ABUSEIPDB_API_KEY


# Fonction pour vérifier si une IP est malveillante
def check_ip_abuse(ip):
    url = f'https://api.abuseipdb.com/api/v2/check'
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    params = {'ipAddress': ip, 'maxAgeInDays': '90'}  # Vérifier dans les 90 derniers jours
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['data']['abuseConfidenceScore'] > 50:  # Score de confiance de malveillance supérieur à 50
            return True
    return False


# Fonction pour traiter un fichier pcap
def analyse_pcap_with_abuseIPDB(pcap_file):
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(IP):  # Vérifier si le paquet contient une couche IP
            ip_dest = packet[IP].dst
            if check_ip_abuse(ip_dest):  # Vérifier si l'IP de destination est malveillante
                print(f"IP malveillante détectée: {ip_dest}")
                alert = "malicious_ip"
                return alert
                
"""
alert= analyse_pcap_with_abuseIPDB("../../Téléchargements/Extrait/ext_1.pcap")
print(alert)
"""