import scapy.all as scapy
import os
import random

# Configuration
save_dir = "dossier_local/Captures"
os.makedirs(save_dir, exist_ok=True)
packet_count = 0


def packet_callback(packet):
    """
    Retrieve requests and save them in PCAP files on the format : id_machine_packet_count.pcap
    """
    global packet_count
    if packet_count >= 1000000:
        packet_count = 0

    # Name and create the file
    filename = os.path.join(save_dir, f"1_{packet_count}.pcap")
    scapy.wrpcap(filename, packet)

    print(f"Package captured and saved in {filename}")
    packet_count += 1


def get_pcap_file():
    """
    Get the next PCAP file, who will be analyse.
    """
    files = [f for f in os.listdir(save_dir) if f.endswith(".pcap")]

    if not files:
        return None

    # Sort by the creation date
    files.sort(key=lambda f: os.path.getctime(os.path.join(save_dir, f)))

    return os.path.join(save_dir, files[0])


if __name__ == '__main__':
    print(f"Capture in progress...")
    scapy.sniff(prn=packet_callback, store=False)