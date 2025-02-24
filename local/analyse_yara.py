import yara
from scapy.all import rdpcap, wrpcap, Raw

def is_malicious(packet):
    if packet.haslayer(Raw):  #Check if packets contain a payload
        payload = bytes(packet[Raw].load)  #Extract payload
        matches = rules.match(data=payload)  #Apply yara rules
        if matches:
            print(f"YARA detected {matches} in a packet")
            return True
    return False

# Load yara rules
rules = yara.compile(filepath="rules/yara-rules-full.yar")

# Load pcap file
packets = rdpcap("ADD PATH TO PCAP FILE HERE")

# Save suspicious packets path
path_results = "ADD PATH TO A SAVE DESTINATION"

suspicious_packets = []

# Get suspicious_packets
for pkt in packets:
    if is_malicious(pkt):
        suspicious_packets.append(pkt)

# Save suspicious packets in a file
if suspicious_packets:
    wrpcap(path_results, suspicious_packets)
    print(f"Extraction done, {len(suspicious_packets)} suspicious packets save in {path_results}")
else:
    print("No suspicious packets found")
