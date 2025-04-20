import re
from scapy.all import rdpcap, TCP, UDP, IP

# Load Snort rules and parse them taking into account continued lines
def load_snort_rules(file_path):
    rules = []
    rule_buffer = ""  # Stores the current rule

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            if line.startswith("alert"):  # New rule detected
                if rule_buffer:  # If a previous rule exists, process it
                    parsed_rule = parse_snort_rule(rule_buffer)
                    if parsed_rule:
                        rules.append(parsed_rule)
                rule_buffer = line  # Start a new rule
            else:
                rule_buffer += " " + line  # Add following lines to the current rule

        # Add the last rule after the loop
        if rule_buffer:
            parsed_rule = parse_snort_rule(rule_buffer)
            if parsed_rule:
                rules.append(parsed_rule)

    return rules

# Function to extract information from a Snort rule
def parse_snort_rule(rule):
    parsed_rule = {}

    # Extraction of the protocol (TCP, UDP, ICMP, IP)
    proto_match = re.search(r'alert (\w+) ', rule)
    parsed_rule["protocol"] = proto_match.group(1) if proto_match else "ip"

    # Extraction of IPs and ports (supporting "any")
    ip_port_match = re.search(r' (\S+) (\S+) -> (\S+) (\S+) ', rule)
    if ip_port_match:
        src_ip, src_port, dst_ip, dst_port = ip_port_match.groups()
        parsed_rule["src_ip"] = None if src_ip == "any" else src_ip
        parsed_rule["src_port"] = None if src_port == "any" else int(src_port) if src_port.isdigit() else None
        parsed_rule["dst_ip"] = None if dst_ip == "any" else dst_ip
        parsed_rule["dst_port"] = None if dst_port == "any" else int(dst_port) if dst_port.isdigit() else None
    else:
        parsed_rule["src_ip"], parsed_rule["src_port"], parsed_rule["dst_ip"], parsed_rule["dst_port"] = None, None, None, None

    # Extraction of "content" signatures (handling hexadecimal values)
    content_matches = re.findall(r'content:"([^"]+)";', rule)
    hex_matches = re.findall(r'content:(.*?)\s*;', rule)  # Search for hexadecimal values

    extracted_contents = []
    for match in hex_matches:
        match = match.strip()
        if match.startswith('"') and match.endswith('"'):
            extracted_contents.append(match.strip('"'))
        elif '|' in match:
            converted_content = convert_snort_hex(match)
            extracted_contents.append(converted_content)

    # Store the content in the rule
    parsed_rule["content"] = extracted_contents[0] if len(extracted_contents) == 1 else extracted_contents

    # Extraction of the message
    msg_match = re.search(r'msg:"([^"]+)";', rule)
    parsed_rule["msg"] = msg_match.group(1) if msg_match else "Alert"

    # If no source IP, destination IP, or content is found, ignore the rule
    if not any([parsed_rule["src_ip"], parsed_rule["dst_ip"], parsed_rule["content"]]):
        return None

    return parsed_rule


# Function to convert Snort hexadecimal format to plain text
def convert_snort_hex(content):
    parts = content.split('|')
    converted = ""
    for i, part in enumerate(parts):
        if i % 2 == 0:
            converted += part  # Texte normal
        else:
            hex_values = part.strip().split()
            converted += "".join(chr(int(h, 16)) for h in hex_values)  # Convert to text
    return converted


def analyse_pcap_with_snort(pcap_path, rules):
    """
    Scans a PCAP file using Snort rules and returns only alert names.
    
    :param pcap_path : the path to the pcap file who needed to be analysed.
    :param rules : rules Snort already parse.
    """
    packets = rdpcap(pcap_path)
    alert_names = set()

    # Analyse each packet
    for pkt in packets:
        # Extract IP, destination, protocol, and payload
        if pkt.haslayer(IP):
            pkt_ip = pkt[IP].src
            pkt_dst = pkt[IP].dst
            pkt_proto = "TCP" if pkt.haslayer(TCP) else "UDP" if pkt.haslayer(UDP) else "IP"
            pkt_payload = bytes(pkt[TCP].payload).decode(errors='ignore') if pkt.haslayer(TCP) else bytes(pkt[UDP].payload).decode(errors='ignore') if pkt.haslayer(UDP) else ""

            best_match = None   # Store the best alert found for this package   

            # Check each rule
            for rule in rules:

                # Check protocol
                if rule["protocol"].upper() == pkt_proto:

                    # Check IPs
                    if rule["src_ip"] and pkt_ip not in rule["src_ip"]:
                        continue

                    # Check destination IPs
                    if rule["dst_ip"] and pkt_dst not in rule["dst_ip"]:
                        continue

                    # Check content
                    if rule["content"]:

                        # Check if content is in the payload and if all content is in too
                        if isinstance(rule["content"], str) and rule["content"] not in pkt_payload:
                            continue
                        elif isinstance(rule["content"], list) and not all(content in pkt_payload for content in rule["content"]):
                            continue

                    # Check if the content is not empty  
                    if isinstance(rule["content"], list) and rule["content"]:
                        detected_content = max(rule["content"], key=len)
                    elif isinstance(rule["content"], str):
                        detected_content = rule["content"]    
                    else:
                            detected_content = ""

                    # If all conditions are met, add an alert
                    if best_match is None or len(detected_content) > len(best_match[1]):
                        best_match = (rule["msg"], detected_content)

            if best_match:
                print(f"\n ALERT : {best_match[0]}")
                print(f" - Package in question : {pkt.summary()}")
                alert_names.add(best_match[0])
            else: 
                return False

    return list(alert_names)[0] if alert_names else None


'''rules_file = "Rules/snort3-community.rules"
pcap_file = "../Téléchargements/Extrait/ext_3.pcap"
rules = load_snort_rules(rules_file)
alerts = analyse_pcap_with_snort(pcap_file, rules)'''
