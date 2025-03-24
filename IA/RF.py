import numpy as np
import pandas as pd
import pickle
import time
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


def test(X_train, X_test, y_train, y_test, correlation, model_name):
    print(model_name)
    if os.path.getsize(f"data_selection/{correlation}") <= 0:
        print("Correlation empty")
    else:
        columns_to_keep = pd.read_csv(f"data_selection/{correlation}", header=None)[0].tolist()
        X_train = X_train[columns_to_keep]
        X_test = X_test[columns_to_keep]

        rf = RandomForestClassifier()

        print("train")
        start_time = time.time()
        rf.fit(X_train, y_train)
        end_time = time.time()
        print("training time: ", end_time - start_time)

        print("predict")
        start_time = time.time()
        y_pred = rf.predict(X_test)
        end_time = time.time()
        print("predict time: ", end_time - start_time)

        print("accuracy")
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy * 100:.2f}%")

        print("rapport")
        print(classification_report(y_test, y_pred))

        print("save the model")
        with open(f"model/{model_name}", "wb") as file:
            pickle.dump(rf, file)

def auto_test(num):
    print("#===-----------------------------------------------------------------------------------------------------------===#")
    dataset = pd.read_csv(f'clean_dataset/dataset_{num}.csv')
    X = dataset.drop(columns='Label')
    y = dataset['Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    files = os.listdir("data_selection")
    num_files = [file for file in files if file.startswith(num)]
    for file in num_files:
        test(X_train, X_test, y_train, y_test, file, f"rf_{file}")

def auto_create(num, corr):
    print("#===-----------------------------------------------------------------------------------------------------------===#")
    dataset = pd.read_csv(f'clean_dataset/dataset_{num}.csv')
    X = dataset.drop(columns='Label')
    y = dataset['Label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    file = f"{corr}.csv"
    test(X_train, X_test, y_train, y_test, file, f"rf_{num}.pkl")

def main():
    #auto_test("0")
    #auto_test("1")
    #auto_test("2")
    #auto_test("3")
    #auto_test("4")
    #auto_test("5")
    #auto_test("6")
    #auto_test("7")

    auto_create("0", "030")
    #auto_create("1", "106")
    #auto_create("2", "202")
    #auto_create("3", "320")
    #auto_create("4", "404")
    #auto_create("5", "530")
    #auto_create("6", "630")
    #auto_create("7", "770")


if __name__ == "__main__":
    main()
