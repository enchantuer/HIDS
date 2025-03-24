import pickle
import numpy as np
import os

import pandas as pd
import pyshark


def get_data(pcap_files, model_num):
    return 0

def predict_model(data, model_num):
    return 0

def predict(pcap_files):

    return 0



def main():
    model = pickle.load(open('model/rf_7.pkl', 'rb'))
    df = pd.read_csv("output.csv")
    select = pd.read_csv("data_selection/770.csv", header=None)
    df = df[select[0].tolist()]
    k = model.predict(df)
    print(k)

if __name__ == "__main__":
    main()