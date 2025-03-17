import re
import os
import shutil
from scapy.all import rdpcap, TCP, UDP, IP, wrpcap

# Global variables
MACHINE_NUMBER = 1
ALERT_COUNTER_FILE = "counter/snort_alert_counter.txt"
MALICIOUS_FOLDER = "malicious"
PCAP_DIRECTORY = "pcap"
SNORT_RULES_FILE = "Rules/snort3-community-rules/snort3-community.rules"

# Load the alert counter
if os.path.exists(ALERT_COUNTER_FILE):
    with open(ALERT_COUNTER_FILE, "r") as f:
        ALERT_COUNTER = int(f.read().strip())
else:
    ALERT_COUNTER = 1

# Load Snort rules
def load_snort_rules(file_path):
    rules = []
    rule_buffer = ""
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("alert"):
                if rule_buffer:
                    parsed_rule = parse_snort_rule(rule_buffer)
                    if parsed_rule:
                        rules.append(parsed_rule)
                rule_buffer = line
            else:
                rule_buffer += " " + line
        if rule_buffer:
            parsed_rule = parse_snort_rule(rule_buffer)
            if parsed_rule:
                rules.append(parsed_rule)
    return rules

# Extract Snort rule components
def parse_snort_rule(rule):
    parsed_rule = {}
    proto_match = re.search(r'alert (\w+) ', rule)
    parsed_rule["protocol"] = proto_match.group(1) if proto_match else "ip"
    ip_port_match = re.search(r' (\S+) (\S+) -> (\S+) (\S+) ', rule)
    if ip_port_match:
        src_ip, src_port, dst_ip, dst_port = ip_port_match.groups()
        parsed_rule["src_ip"] = None if src_ip == "any" else src_ip
        parsed_rule["src_port"] = None if src_port == "any" else int(src_port) if src_port.isdigit() else None
        parsed_rule["dst_ip"] = None if dst_ip == "any" else dst_ip
        parsed_rule["dst_port"] = None if dst_port == "any" else int(dst_port) if dst_port.isdigit() else None
    else:
        parsed_rule["src_ip"], parsed_rule["src_port"], parsed_rule["dst_ip"], parsed_rule["dst_port"] = None, None, None, None
    content_matches = re.findall(r'content:"([^"]+)";', rule)
    parsed_rule["content"] = content_matches if content_matches else None
    msg_match = re.search(r'msg:"([^"]+)";', rule)
    parsed_rule["msg"] = msg_match.group(1) if msg_match else "Alert"
    if not any([parsed_rule["src_ip"], parsed_rule["dst_ip"], parsed_rule["content"]]):
        return None
    return parsed_rule

# Function to analyse PCAP files
def analyse_pcap(pcap_path, rules):
    global ALERT_COUNTER
    packets = rdpcap(pcap_path)

    detected_alerts = []
    for pkt in packets:
        if pkt.haslayer(IP):
            pkt_ip = pkt[IP].src
            pkt_dst = pkt[IP].dst
            pkt_proto = "TCP" if pkt.haslayer(TCP) else "UDP" if pkt.haslayer(UDP) else "IP"
            pkt_payload = bytes(pkt[TCP].payload).decode(errors='ignore') if pkt.haslayer(TCP) else bytes(pkt[UDP].payload).decode(errors='ignore') if pkt.haslayer(UDP) else ""

            for rule in rules:
                if rule["protocol"].upper() == pkt_proto:
                    if rule["src_ip"] and pkt_ip != rule["src_ip"]:
                        continue
                    if rule["dst_ip"] and pkt_dst != rule["dst_ip"]:
                        continue
                    if rule["content"] and not any(content in pkt_payload for content in rule["content"]):
                        continue

                    attack_name = rule["msg"].replace(" ", "_")
                    detected_alerts.append((pkt, attack_name))

    if detected_alerts:
        if not os.path.exists(MALICIOUS_FOLDER):
            os.makedirs(MALICIOUS_FOLDER)

        for pkt, attack_name in detected_alerts:
            new_filename = f"{MACHINE_NUMBER}_{ALERT_COUNTER}_snort_{attack_name}.pcap"
            wrpcap(os.path.join(MALICIOUS_FOLDER, new_filename), pkt)
            ALERT_COUNTER += 1

        with open(ALERT_COUNTER_FILE, "w") as f:
            f.write(str(ALERT_COUNTER))
        return True
    return False

if os.path.exists(SNORT_RULES_FILE):
    rules = load_snort_rules(SNORT_RULES_FILE)
else:
    print(f"Error: Snort rules file {SNORT_RULES_FILE} not found.")
    exit()

# Scan all PCAP files in the directory
if os.path.exists(PCAP_DIRECTORY):
    for pcap_file in os.listdir(PCAP_DIRECTORY):
        if pcap_file.endswith(".pcap"):
            pcap_path = os.path.join(PCAP_DIRECTORY, pcap_file)
            if analyse_pcap(pcap_path, rules):
                print(f"File {pcap_file} detected as malicious and saved.")
            else:
                print(f"File {pcap_file} not detected as malicious.")
else:
    print(f"Error: PCAP directory {PCAP_DIRECTORY} not found.")
    exit()
