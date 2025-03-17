import os
import yara
from scapy.all import rdpcap, wrpcap, Raw

# Global variables
MACHINE_NUMBER = 1
ALERT_COUNTER_FILE = "counter/yara_alert_counter.txt"
MALICIOUS_FOLDER = "malicious"
PCAP_DIRECTORY = "pcap"
YARA_RULES_FILE = "Rules/yara-rules-full.yar"

# Load the alert counter
if os.path.exists(ALERT_COUNTER_FILE):
    with open(ALERT_COUNTER_FILE, "r") as f:
        ALERT_COUNTER = int(f.read().strip())
else:
    ALERT_COUNTER = 1

# Load YARA rules
if os.path.exists(YARA_RULES_FILE):
    rules = yara.compile(filepath=YARA_RULES_FILE)
else:
    print(f"Error: YARA rules file {YARA_RULES_FILE} not found.")
    exit()

# Function to check if a packet is malicious
def is_malicious(packet):
    if packet.haslayer(Raw):
        payload = bytes(packet[Raw].load)
        matches = rules.match(data=payload)
        if matches:
            return [match.rule for match in matches]
    return []

# Function to analyse PCAP files
def analyse_pcap(pcap_path):
    global ALERT_COUNTER
    packets = rdpcap(pcap_path)
    malicious_packets = []

    for pkt in packets:
        matched_rules = is_malicious(pkt)
        if matched_rules:
            malicious_packets.append((pkt, matched_rules[0]))  # Only save the first rule

    if malicious_packets:
        if not os.path.exists(MALICIOUS_FOLDER):
            os.makedirs(MALICIOUS_FOLDER)

        for pkt, rule_name in malicious_packets:
            attack_name = rule_name.replace(" ", "_")
            new_filename = f"{MACHINE_NUMBER}_{ALERT_COUNTER}_yara_{attack_name}.pcap"
            wrpcap(os.path.join(MALICIOUS_FOLDER, new_filename), [pkt])
            ALERT_COUNTER += 1

        with open(ALERT_COUNTER_FILE, "w") as f:
            f.write(str(ALERT_COUNTER))

        return True
    return False

# Scan all PCAP files in the directory
if os.path.exists(PCAP_DIRECTORY):
    for pcap_file in os.listdir(PCAP_DIRECTORY):
        if pcap_file.endswith(".pcap"):
            pcap_path = os.path.join(PCAP_DIRECTORY, pcap_file)
            if analyse_pcap(pcap_path):
                print(f"File {pcap_file} detected as malicious and saved.")
            else:
                print(f"File {pcap_file} not detected as malicious.")
else:
    print(f"Error: PCAP directory {PCAP_DIRECTORY} not found.")
    exit()
