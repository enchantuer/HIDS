import yara
from scapy.all import rdpcap, TCP, UDP, wrpcap, Raw

def extract_payload(pkt):
    """
    Extracts payload (payload) from a packet by checking multiple layers (Raw, TCP, UDP).
    :param pkt: The Scapy packet.
    :return: Payload in bytes or None if there is no payload.
    """
    # Checks the raw layer
    if pkt.haslayer(Raw):
        return bytes(pkt[Raw].load)

    # Checks payload in TCP or UDP layers
    elif pkt.haslayer(TCP) and pkt[TCP].payload:
        return bytes(pkt[TCP].payload)

    elif pkt.haslayer(UDP) and pkt[UDP].payload:
        return bytes(pkt[UDP].payload)

    return None


def analyse_pcap_with_yara(pcap_path, yara_rules_path):
    """
    Scans a PCAP file with YARA rules and returns the detected alerts.
    :param pcap_path: Path of the PCAP file to be analyzed.
    :param yara_rules_path: Path to the file containing the YARA rules.
    :return: Tuple (alert name, package summary) if an alert is detected, otherwise None.
    """
    try:
        # Load the YARA rules
        rules = yara.compile(filepath=yara_rules_path)
    except yara.SyntaxError as e:
        print(f"Error of syntax in YARA rules : {e}")
        return None

    try:
        # Load the PCAP file
        packets = rdpcap(pcap_path)
        if len(packets) == 0:
            print("The PCAP file is empty.")
            return None
    except Exception as e:
        print(f"Error in the reading of the PCAP file : {e}")
        return None

    # Browse each package and extract the payload
    for pkt in packets:
        payload = extract_payload(pkt)
        
        if payload:
            # Application of YARA rules on the payload
            matches = rules.match(data=payload)

            if matches:
                for match in matches:
                    alert_name = match.rule
                    packet_summary = pkt.summary()

                    # Print the alert
                    print(f"\n ALERT : {alert_name}")
                    print(f" - Package in question : {packet_summary}")
                    return alert_name
    return None


"""
pcap_file = "../Téléchargements/Extrait/ext_7.pcap"
yara_rules_file = "Rules/yara-rules-full.yar"
analyse_pcap_with_yara(pcap_file, yara_rules_file)
"""
