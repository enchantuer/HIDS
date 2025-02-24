import re
import json


def load_suricata_rules(file_path):
    """
    Function to load and parse Suricata rules in a json file.

    :param file_path : the path to the original rules file of suricata (.rules).
    """
    rules = []
    rule_buffer = ""

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if line.startswith("alert"):  # New rule detected
                if rule_buffer:
                    parsed_rule = parse_suricata_rule(rule_buffer)
                    if parsed_rule:
                        rules.append(parsed_rule)
                rule_buffer = line  # CStart a new rule
            else:
                rule_buffer += " " + line  # Add the following lines to the current rule

        if rule_buffer:  # Add last rule after loop
            parsed_rule = parse_suricata_rule(rule_buffer)
            if parsed_rule:
                rules.append(parsed_rule)

    print(f"{len(rules)} Suricata rules extracted and recorded in suricata_rules.json")
    return rules


def parse_suricata_rule(rule):
    """
    Function to extract information from a Suricata rule. 

    :param rule : the content of one rule.
    """
    parsed_rule = {}

    # Extraction of alert name
    msg_match = re.search(r'msg:"(.*?)";', rule)
    parsed_rule["name"] = msg_match.group(1) if msg_match else "Unknown"

    # Extraction of the protocole (TCP, UDP, ICMP, IP)
    proto_match = re.search(r'alert (\w+) ', rule)
    parsed_rule["protocol"] = proto_match.group(1) if proto_match else "ip"

    # Extraction of IP addresses and ports
    ip_port_match = re.search(r' (\S+) (\S+) -> (\S+) (\S+) ', rule)
    if ip_port_match:
        src_ip, src_port, dst_ip, dst_port = ip_port_match.groups()
        parsed_rule["src_ip"] = None if src_ip == "any" else src_ip
        parsed_rule["src_port"] = None if src_port == "any" else src_port
        parsed_rule["dst_ip"] = None if dst_ip == "any" else dst_ip
        parsed_rule["dst_port"] = None if dst_port == "any" else dst_port
    else:
        parsed_rule["src_ip"], parsed_rule["src_port"], parsed_rule["dst_ip"], parsed_rule["dst_port"] = None, None, None, None

    # Content extraction (hex values management)
    content_matches = re.findall(r'content:"(.*?)";', rule)
    parsed_rule["content"] = [convert_suricata_hex(c) for c in content_matches]

    return parsed_rule


def convert_suricata_hex(content):
    """
    Function to convert the hexadecimal format Suricata in plain text.

    :param content : the content that needs to be converted to hexadecimal format.
    """
    parts = content.split('|')
    converted = ""
    
    for i, part in enumerate(parts):
        if i % 2 == 0:
            converted += part  # Normal text
        else:
            hex_values = part.strip().split()
            for h in hex_values:
                try:
                    char_value = int(h, 16)
                    if 0x00 <= char_value <= 0x10FFFF:  # Checking the Unicode range
                        converted += chr(char_value)
                    else:
                        print(f"Warning: hex value out of range Unicode ignored -> {h}")
                except ValueError:
                    print(f"Warning: Invalid hex value ignored -> {h}")

    return converted


def optimize_suricata_rules(input_file, output_file):
    """
    Optimizes the Suricata rules file by filtering non-critical categories and removing redundant or overly generic rules.

    :param input_file: Path of the JSON file containing the Suricata rules
    :param output_file: Path of the JSON file where to save optimized rules
    """
    # Load the JSON file of the Suricata rules
    with open(input_file, "r", encoding="utf-8") as f:
        rules = json.load(f)

    # Filter criteria
    categories_importantes = [
        "ET EXPLOIT", "ET MALWARE", "ET ATTACK_RESPONSE",
        "ET TROJAN", "ET CnC", "ET SHELLCODE", "ET WEB_EXPLOIT"
    ]
    min_content_length = 5  # Exclude content that is too short
    filtered_rules = {}  # Dictionary to avoid duplicates

    for rule in rules:
        rule_name = rule["name"]

        # Check if the rule belongs to an important category
        if not any(category in rule_name for category in categories_importantes):
            continue  # Ignorer cette règle

        # Filter too short content
        rule["content"] = [c for c in rule.get("content", []) if len(c) >= min_content_length]
        if not rule["content"]:  # If no relevant content remains, ignore the rule
            continue

        # Merge similar rules by deleting numbers 
        rule_key = rule_name.split("(")[0].strip()
        if rule_key in filtered_rules:
            filtered_rules[rule_key]["content"].extend(rule["content"])
        else:
            filtered_rules[rule_key] = rule

    # Save optimized rules in a new file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(list(filtered_rules.values()), f, indent=4)

    print(f" Optimized rules : {len(filtered_rules)} rules saved in {output_file}")



if __name__ == '__main__':

    # Saving parsed Suricata rules in a JSON file
    rules = load_suricata_rules("emerging-all.rules")
    with open("suricata_rules.json", "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=4)

    # Use of the optimization function 
    input_file = "suricata_rules.json"
    output_file = "suricata_rules_optimized.json"
    optimize_suricata_rules(input_file, output_file)