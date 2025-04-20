import pickle
import numpy as np
import os
import sys
import pandas as pd
import pyshark
from collections import defaultdict
from tqdm import tqdm


def get_data(pcap_files, model_num):
    return 0

def predict_model(data, model_num):
    return 0

def convert(pcap_files):
    pcap_file = f"{pcap_files}"
    cap = pyshark.FileCapture(pcap_file, display_filter="ip")

    flows = defaultdict(list)

    # === Extract Packets ===
    for packet in tqdm(cap, desc="Processing Packets", disable=True):
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
            "Fwd Packets Length Total": sum(sizes) if sizes else 0,
        })

    # === Save as CSV ===
    df = pd.DataFrame(flow_features)

    # === Remove Unwanted Columns ===
    columns_to_remove = ["Flow ID", "Fwd Header Length.1", "Source IP", "Src IP",
                         "Source Port", "Src Port", "Destination IP", "Dst IP",
                         "Destination Port", "Dst Port" , "Timestamp"]

    df = df.drop(columns=[col for col in columns_to_remove if col in df], errors="ignore")

    return df

def predict(pcap_df, model, corr):
    model = pickle.load(open(f'dossier_local/ia/model/{model}', 'rb'))
    select = pd.read_csv(f"dossier_local/ia/data_selection/{corr}", header=None)
    df = pcap_df[select[0].tolist()]
    k = model.predict(df)
    return k

def return_name_attack(results):
    attack_name = []
    for result in results:
        if result != "BENIGN":
            attack_name = result
            return attack_name
    return None

def prediction_with_random_forest(pcap_file):
    result = []
    df = convert(pcap_file)
    result.extend(predict(df, "rf_0.pkl", "030.csv").tolist())
    result.extend(predict(df, "rf_1.pkl", "106.csv").tolist())
    result.extend(predict(df, "rf_2.pkl", "202.csv").tolist())
    result.extend(predict(df, "rf_3.pkl", "320.csv").tolist())
    result.extend(predict(df, "rf_4.pkl", "404.csv").tolist())
    result.extend(predict(df, "rf_5.pkl", "530.csv").tolist())
    result.extend(predict(df, "rf_6.pkl", "630.csv").tolist())
    result.extend(predict(df, "rf_7.pkl", "770.csv").tolist())
    attack_name = return_name_attack(result)
    return attack_name

def prediction_with_support_vector_machine(pcap_file):
    result = []
    df = convert(pcap_file)
    result.extend(predict(df, "svm_0.pkl", "030.csv").tolist())
    result.extend(predict(df, "svm_1.pkl", "190.csv").tolist())
    result.extend(predict(df, "svm_2.pkl", "204.csv").tolist())
    result.extend(predict(df, "svm_3.pkl", "330.csv").tolist())
    result.extend(predict(df, "svm_4.pkl", "402.csv").tolist())
    result.extend(predict(df, "svm_5.pkl", "520.csv").tolist())
    result.extend(predict(df, "svm_6.pkl", "650.csv").tolist())
    result.extend(predict(df, "svm_7.pkl", "770.csv").tolist())
    attack_name = return_name_attack(result)
    return attack_name



"""print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_1.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_2.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_3.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_4.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_5.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_6.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_7.pcap"))
print(prediction_with_random_forest("../../Téléchargements/Extrait/ext_8.pcap"))

print("-------------------------")
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_1.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_2.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_3.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_4.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_5.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_6.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_7.pcap"))
print(prediction_with_support_vector_machine("../../Téléchargements/Extrait/ext_8.pcap"))"""
