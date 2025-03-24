import pyshark
import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm

# === Load PCAP File ===
pcap_file = "pcap_files/ext_1.pcap"
cap = pyshark.FileCapture(pcap_file, display_filter="ip")

# === Initialize Storage for Network Flows ===
flows = defaultdict(list)

# === Extract Packets ===
for packet in tqdm(cap, desc="Processing Packets"):
    try:
        protocol = packet.transport_layer
        timestamp = float(packet.sniff_timestamp)
        packet_length = int(packet.length)

        flow_id = f"{protocol}"

        flows[flow_id].append({
            "timestamp": timestamp,
            "packet_length": packet_length,
            "flags": packet.tcp.flags if protocol == "TCP" else None,
            "header_length": int(packet.ip.hdr_length) if hasattr(packet.ip, "hdr_length") else 0
        })
    except AttributeError:
        continue  # Skip non-IP packets

# === Compute Flow Statistics ===
flow_features = []

for flow_id, packets in flows.items():
    timestamps = [pkt["timestamp"] for pkt in packets]
    sizes = [pkt["packet_length"] for pkt in packets]
    flags = [pkt["flags"] for pkt in packets if pkt["flags"] is not None]
    header_sizes = [pkt["header_length"] for pkt in packets]

    # Flow Duration & IAT
    duration = max(timestamps) - min(timestamps) if len(timestamps) > 1 else 0
    iat = np.diff(timestamps) if len(timestamps) > 1 else [0]

    # === Flow Feature Calculations ===
    flow_features.append({
        # Packet Length Features
        "Flow Duration": duration,
        "Fwd Packet Length Max": max(sizes),
        "Fwd Packet Length Mean": np.mean(sizes),
        "Fwd Packet Length Std": np.std(sizes),
        "Fwd Packet Length Min": min(sizes),
        "Packet Length Max": max(sizes),
        "Packet Length Min": min(sizes),
        "Packet Length Mean": np.mean(sizes),
        "Packet Length Std": np.std(sizes),
        "Packet Length Variance": np.var(sizes),

        # Inter-Arrival Time (IAT) Features
        "Flow IAT Mean": np.mean(iat),
        "Flow IAT Std": np.std(iat),
        "Flow IAT Max": max(iat),
        "Flow Bytes/s": sum(sizes) / duration if duration > 0 else 0,

        # Flag Counts
        "ACK Flag Count": flags.count("0x10") if flags else 0,
        "RST Flag Count": flags.count("0x04") if flags else 0,
        "ECE Flag Count": flags.count("0x40") if flags else 0,
        "FIN Flag Count": flags.count("0x01") if flags else 0,
        "URG Flag Count": flags.count("0x20") if flags else 0,
        "PSH Flag Count": flags.count("0x08") if flags else 0,

        # Segment Size Features
        "Avg Fwd Segment Size": np.mean(sizes) if sizes else 0,
        "Avg Bwd Segment Size": np.mean(sizes) if sizes else 0,
        "Subflow Fwd Packets": len(sizes),
        "Subflow Bwd Packets": len(sizes),
        "Subflow Fwd Bytes": sum(sizes) if sizes else 0,

        # Additional Features (calculated from available data)
        "Avg Packet Size": np.mean(sizes) if sizes else 0,
        "Avg Bwd Segment Size": np.mean(sizes) if sizes else 0,
        "Total Fwd Packets": len(sizes),
        "Total Backward Packets": len(sizes),
        "Bwd Packet Length Max": max(sizes) if sizes else 0,
        "Bwd Packet Length Min": min(sizes) if sizes else 0,
        "Bwd Packet Length Mean": np.mean(sizes) if sizes else 0,
        "Bwd Packet Length Std": np.std(sizes) if sizes else 0,

        # Additional Features for Segment & Header Sizes
        "Init Fwd Win Bytes": sum(header_sizes) if header_sizes else 0,
        "Init Bwd Win Bytes": sum(header_sizes) if header_sizes else 0,
        "Fwd Act Data Packets": len([pkt for pkt in packets if pkt.get('flags')]),
        "Fwd Seg Size Min": min(sizes) if sizes else 0,
        "Bwd IAT Mean": np.mean(iat) if len(iat) > 0 else 0,
        "Bwd IAT Min": min(iat) if len(iat) > 0 else 0,
        "Fwd Seg Size Min": min(sizes) if sizes else 0,
        "Fwd Header Length": sum(header_sizes) if header_sizes else 0,
        "Bwd Header Length": sum(header_sizes) if header_sizes else 0,
    })

# === Save as CSV ===
df = pd.DataFrame(flow_features)

# === Remove Unwanted Columns ===
columns_to_remove = ["Flow ID", "Fwd Header Length.1", "Source IP", "Src IP",
                     "Source Port", "Src Port", "Destination IP", "Dst IP",
                     "Destination Port", "Dst Port", "Timestamp"]

df = df.drop(columns=[col for col in columns_to_remove if col in df], errors="ignore")

df.to_csv("output.csv", index=True)
print("File saved")
