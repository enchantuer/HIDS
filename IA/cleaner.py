import numpy as np
import pandas as pd
import dask.dataframe as dd
import os
from fastai.tabular.all import df_shrink
from fastcore.parallel import *

col_name_consistency = {
'Flow ID': 'Flow ID',
'Source IP': 'Source IP',
'Src IP':  'Source IP',
'Source Port': 'Source Port',
'Src Port': 'Source Port',
'Destination IP': 'Destination IP',
'Dst IP': 'Destination IP',
'Destination Port': 'Destination Port',
'Dst Port': 'Destination Port',
'Protocol': 'Protocol',
'Timestamp': 'Timestamp',
'Flow Duration': 'Flow Duration',
'Total Fwd Packets': 'Total Fwd Packets',
'Tot Fwd Pkts': 'Total Fwd Packets',
'Total Backward Packets': 'Total Backward Packets',
'Tot Bwd Pkts': 'Total Backward Packets',
'Total Length of Fwd Packets': 'Fwd Packets Length Total',
'TotLen Fwd Pkts': 'Fwd Packets Length Total',
'Total Length of Bwd Packets': 'Bwd Packets Length Total',
'TotLen Bwd Pkts': 'Bwd Packets Length Total',
'Fwd Packet Length Max': 'Fwd Packet Length Max',
'Fwd Pkt Len Max': 'Fwd Packet Length Max',
'Fwd Packet Length Min': 'Fwd Packet Length Min',
'Fwd Pkt Len Min': 'Fwd Packet Length Min',
'Fwd Packet Length Mean': 'Fwd Packet Length Mean',
'Fwd Pkt Len Mean': 'Fwd Packet Length Mean',
'Fwd Packet Length Std': 'Fwd Packet Length Std',
'Fwd Pkt Len Std': 'Fwd Packet Length Std',
'Bwd Packet Length Max': 'Bwd Packet Length Max',
'Bwd Pkt Len Max': 'Bwd Packet Length Max',
'Bwd Packet Length Min': 'Bwd Packet Length Min',
'Bwd Pkt Len Min': 'Bwd Packet Length Min',
'Bwd Packet Length Mean': 'Bwd Packet Length Mean',
'Bwd Pkt Len Mean': 'Bwd Packet Length Mean',
'Bwd Packet Length Std': 'Bwd Packet Length Std',
'Bwd Pkt Len Std': 'Bwd Packet Length Std',
'Flow Bytes/s': 'Flow Bytes/s',
'Flow Byts/s': 'Flow Bytes/s',
'Flow Packets/s': 'Flow Packets/s',
'Flow Pkts/s': 'Flow Packets/s',
'Flow IAT Mean': 'Flow IAT Mean',
'Flow IAT Std': 'Flow IAT Std',
'Flow IAT Max': 'Flow IAT Max',
'Flow IAT Min': 'Flow IAT Min',
'Fwd IAT Total': 'Fwd IAT Total',
'Fwd IAT Tot': 'Fwd IAT Total',
'Fwd IAT Mean': 'Fwd IAT Mean',
'Fwd IAT Std': 'Fwd IAT Std',
'Fwd IAT Max': 'Fwd IAT Max',
'Fwd IAT Min': 'Fwd IAT Min',
'Bwd IAT Total': 'Bwd IAT Total',
'Bwd IAT Tot': 'Bwd IAT Total',
'Bwd IAT Mean': 'Bwd IAT Mean',
'Bwd IAT Std': 'Bwd IAT Std',
'Bwd IAT Max': 'Bwd IAT Max',
'Bwd IAT Min': 'Bwd IAT Min',
'Fwd PSH Flags': 'Fwd PSH Flags',
'Bwd PSH Flags': 'Bwd PSH Flags',
'Fwd URG Flags': 'Fwd URG Flags',
'Bwd URG Flags': 'Bwd URG Flags',
'Fwd Header Length': 'Fwd Header Length',
'Fwd Header Len': 'Fwd Header Length',
'Bwd Header Length': 'Bwd Header Length',
'Bwd Header Len': 'Bwd Header Length',
'Fwd Packets/s': 'Fwd Packets/s',
'Fwd Pkts/s': 'Fwd Packets/s',
'Bwd Packets/s': 'Bwd Packets/s',
'Bwd Pkts/s': 'Bwd Packets/s',
'Min Packet Length': 'Packet Length Min',
'Pkt Len Min': 'Packet Length Min',
'Max Packet Length': 'Packet Length Max',
'Pkt Len Max': 'Packet Length Max',
'Packet Length Mean': 'Packet Length Mean',
'Pkt Len Mean': 'Packet Length Mean',
'Packet Length Std': 'Packet Length Std',
'Pkt Len Std': 'Packet Length Std',
'Packet Length Variance': 'Packet Length Variance',
'Pkt Len Var': 'Packet Length Variance',
'FIN Flag Count': 'FIN Flag Count',
'FIN Flag Cnt': 'FIN Flag Count',
'SYN Flag Count': 'SYN Flag Count',
'SYN Flag Cnt': 'SYN Flag Count',
'RST Flag Count': 'RST Flag Count',
'RST Flag Cnt': 'RST Flag Count',
'PSH Flag Count': 'PSH Flag Count',
'PSH Flag Cnt': 'PSH Flag Count',
'ACK Flag Count': 'ACK Flag Count',
'ACK Flag Cnt': 'ACK Flag Count',
'URG Flag Count': 'URG Flag Count',
'URG Flag Cnt': 'URG Flag Count',
'CWE Flag Count': 'CWE Flag Count',
'CWE Flag Cnt': 'CWE Flag Count',
'ECE Flag Count': 'ECE Flag Count',
'ECE Flag Cnt': 'ECE Flag Count',
'Down/Up Ratio': 'Down/Up Ratio',
'Average Packet Size': 'Avg Packet Size',
'Pkt Size Avg': 'Avg Packet Size',
'Avg Fwd Segment Size': 'Avg Fwd Segment Size',
'Fwd Seg Size Avg': 'Avg Fwd Segment Size',
'Avg Bwd Segment Size': 'Avg Bwd Segment Size',
'Bwd Seg Size Avg': 'Avg Bwd Segment Size',
'Fwd Avg Bytes/Bulk': 'Fwd Avg Bytes/Bulk',
'Fwd Byts/b Avg': 'Fwd Avg Bytes/Bulk',
'Fwd Avg Packets/Bulk': 'Fwd Avg Packets/Bulk',
'Fwd Pkts/b Avg': 'Fwd Avg Packets/Bulk',
'Fwd Avg Bulk Rate': 'Fwd Avg Bulk Rate',
'Fwd Blk Rate Avg': 'Fwd Avg Bulk Rate',
'Bwd Avg Bytes/Bulk': 'Bwd Avg Bytes/Bulk',
'Bwd Byts/b Avg': 'Bwd Avg Bytes/Bulk',
'Bwd Avg Packets/Bulk': 'Bwd Avg Packets/Bulk',
'Bwd Pkts/b Avg': 'Bwd Avg Packets/Bulk',
'Bwd Avg Bulk Rate': 'Bwd Avg Bulk Rate',
'Bwd Blk Rate Avg': 'Bwd Avg Bulk Rate',
'Subflow Fwd Packets': 'Subflow Fwd Packets',
'Subflow Fwd Pkts': 'Subflow Fwd Packets',
'Subflow Fwd Bytes': 'Subflow Fwd Bytes',
'Subflow Fwd Byts': 'Subflow Fwd Bytes',
'Subflow Bwd Packets': 'Subflow Bwd Packets',
'Subflow Bwd Pkts': 'Subflow Bwd Packets',
'Subflow Bwd Bytes': 'Subflow Bwd Bytes',
'Subflow Bwd Byts': 'Subflow Bwd Bytes',
'Init_Win_bytes_forward': 'Init Fwd Win Bytes',
'Init Fwd Win Byts': 'Init Fwd Win Bytes',
'Init_Win_bytes_backward': 'Init Bwd Win Bytes',
'Init Bwd Win Byts': 'Init Bwd Win Bytes',
'act_data_pkt_fwd': 'Fwd Act Data Packets',
'Fwd Act Data Pkts': 'Fwd Act Data Packets',
'min_seg_size_forward': 'Fwd Seg Size Min',
'Fwd Seg Size Min': 'Fwd Seg Size Min',
'Active Mean': 'Active Mean',
'Active Std': 'Active Std',
'Active Max': 'Active Max',
'Active Min': 'Active Min',
'Idle Mean': 'Idle Mean',
'Idle Std': 'Idle Std',
'Idle Max': 'Idle Max',
'Idle Min': 'Idle Min',
'Label': 'Label'
}
drop_columns = [
    "Flow ID",
    'Fwd Header Length.1',
    "Source IP", "Src IP",
    "Source Port", "Src Port",
    "Destination IP", "Dst IP",
    "Destination Port", "Dst Port",
    "Timestamp",
]


def remove_useless_columns(dfs):
    for df in dfs:
        df.columns = df.columns.str.strip()
        df.drop(columns=drop_columns, inplace=True, errors='ignore')
        df.rename(columns=col_name_consistency, inplace=True)
        df.replace({'Label': {'Benign': 'BENIGN'}}, inplace=True)
    return dfs

def resize(dfs):
    dfs = parallel(f=df_shrink, items=dfs, progress=True)
    return dfs

def remove_nan(dfs):
    for df in dfs:
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        print(df.isna().any(axis=1).sum(), "rows with at least one NaN to remove")
        df.dropna(inplace=True)
    return dfs

def remove_duplicates(dfs):
    for df in dfs:
        print(df.duplicated().sum(), "fully duplicate rows to remove")
        df.drop_duplicates(inplace=True)
        df.reset_index(inplace=True, drop=True)
    return dfs

def remove_unique_value_columns(dfs):
    unique_value_columns = set()

    # Loop through each DataFrame in the list
    for df in dfs:
        # Find columns with one unique value
        cols_one_value = [col for col in df.columns if df[col].nunique() == 1]
        unique_value_columns.update(cols_one_value)
    unique_value_columns = list(unique_value_columns)
    for df in dfs:
        df.drop(unique_value_columns, axis=1, inplace=True)
    return dfs

def fusion_smilar(dfs):
    grouped_dfs = {}
    for df in dfs:
        key = tuple(sorted(df['Label'].unique()))  # Clé basée sur les valeurs uniques triées
        if key in grouped_dfs:
            grouped_dfs[key].append(df)  # Ajouter le DataFrame au groupe existant
        else:
            grouped_dfs[key] = [df]  # Créer un nouveau groupe

    dfs = [pd.concat(group, ignore_index=True) for group in grouped_dfs.values()]
    return dfs

def add_in_index(df, i):
    index_file = "clean_dataset/index.txt"

    # Extract unique labels
    unique_labels = df["Label"].unique()

    # Append to the index file
    with open(index_file, "a") as f:
        f.write(f"dataset_{i}.csv: {', '.join(map(str, unique_labels))}\n")

def save_dataframes(dfs):
    for i, df in enumerate(dfs):
        df.to_csv(f'clean_dataset/dataset_{i}.csv', index=False)
        print(f"save new dataframe {i}")
        add_in_index(df, i)

def get_data_stat(dfs):
    for i, df in enumerate(dfs):
        print(f"DataFrame {i}:")
        print(f"- Number of rows: {df.shape[0]}")
        print(f"- Number of columns: {df.shape[1]}")

        if "Label" in df.columns:
            print(f"- Unique Label values: {df['Label'].unique().tolist()}")
        else:
            print("- Column 'Label' not found")

        print("---------------------------------------------------")


def main():
    print("begin cleaning data")
    print("get files")
    print("create dataframes")
    dfs = []
    for dirname, _, filenames in os.walk('initial_dataset'):
        for filename in filenames:
            if filename.endswith('.csv'):
                pds = os.path.join(dirname, filename)
                print(pds)
                dask_df = dd.read_csv(pds, assume_missing=True)
                pandas_df = dask_df.compute()
                dfs.append(pandas_df)

    print("remove useless columns")
    dfs = remove_useless_columns(dfs)
    print("remove nan")
    dfs = remove_nan(dfs)
    print("remove duplicate rows")
    dfs = remove_duplicates(dfs)
    print("resize data")
    dfs = resize(dfs)

    print([len(df) for df in dfs])

    print("remove unique values")
    dfs = remove_unique_value_columns(dfs)
    print("fusion similar dataframes")
    dfs = fusion_smilar(dfs)

    print("save dataframes")
    open("clean_dataset/index.txt", "w").close()
    save_dataframes(dfs)
    print("done")
    get_data_stat(dfs)

if __name__ == "__main__":
    main()
