import re
import scapy.all as scapy
import json
from collections import defaultdict
import time

    
def analyse_pcap_with_suricata(pcap_path):
    """
    Scan a pcap file to detect malware from the Suricata rules (json file), returns the name of the alert, 
    the package in question and the comment if it exists.  

    :param pcap_path : the path to the pcap file who needed to be analysed.
    """
    rules_file = "local/rules/suricata_rules_optimized.json"
    with open(rules_file, "r", encoding="utf-8") as f:
        rules = json.load(f)

    packets = scapy.rdpcap(pcap_path)

    for pkt in packets:
        # Ignore packages without payload
        if not pkt.haslayer(scapy.Raw):  
            continue  
        
        payload = bytes(pkt[scapy.Raw].load)
        best_match = None   # Store the best alert per package

        for rule in rules:
            rule_name = rule["name"]
            rule_protocol = rule["protocol"].lower()
            rule_contents = rule.get("content", [])
            rule_src_ip = rule.get("src_ip")
            rule_dst_ip = rule.get("dst_ip")
            rule_src_port = rule.get("src_port")
            rule_dst_port = rule.get("dst_port")

            # Check the protocol
            if rule_protocol == "tcp" and not pkt.haslayer(scapy.TCP):
                continue
            if rule_protocol == "udp" and not pkt.haslayer(scapy.UDP):
                continue

            # Checking IP addresses and ports
            if pkt.haslayer(scapy.IP):
                src_ip = pkt[scapy.IP].src
                dst_ip = pkt[scapy.IP].dst

                if rule_src_ip and rule_src_ip != "any" and rule_src_ip != src_ip:
                    continue
                if rule_dst_ip and rule_dst_ip != "any" and rule_dst_ip != dst_ip:
                    continue

            if pkt.haslayer(scapy.TCP) or pkt.haslayer(scapy.UDP):
                src_port = pkt.sport
                dst_port = pkt.dport

                if rule_src_port and rule_src_port != "any":
                    try:
                        if int(rule_src_port) != src_port:
                            continue
                    except ValueError:
                        pass  # Ignore if port is not a number

                if rule_dst_port and rule_dst_port != "any":
                    try:
                        if int(rule_dst_port) != dst_port:
                            continue
                    except ValueError:
                        pass

            # Check if any of the contents of the rule is present in the package
            for content in rule_contents:
                if len(content) < 4:  # Avoid false positives with too short content
                    continue
                if content.encode() in payload:
                    if best_match is None or len(content) > len(best_match[1]):  
                        # Keep the rule with the longest content (more specific)
                        best_match = (rule_name, content)

        # Show only one alert per package
        if best_match:
            print(f" ALERT : {best_match[0]}")
            print(f" - Package in question : {pkt.summary()}")
            print(f" - Detected content : {best_match[1]}\n")
            return best_match[0]
        else:
            return False



