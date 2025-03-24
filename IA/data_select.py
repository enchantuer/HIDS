import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt


def remove_perfect_correlation(df):
    matrix = df.corr()
    perfect_corr_pairs = []
    for col1 in matrix.columns:
        for col2 in matrix.columns:
            if col1 != col2 and matrix.loc[col1, col2] == 1.0:
                perfect_corr_pairs.append((col1, col2))

    columns_to_drop = []
    for col1, col2 in perfect_corr_pairs:
        corr_with_target_col1 = matrix.loc[col1, 'Label']
        corr_with_target_col2 = matrix.loc[col2, 'Label']

        if abs(corr_with_target_col1) > abs(corr_with_target_col2):
            columns_to_drop.append(col2)
        else:
            columns_to_drop.append(col1)

    df = df.drop(columns=columns_to_drop)

def make_matrix(file_name, attack):
    print(f"matrix for {attack} attack")

    label_encoder = LabelEncoder()

    dataset = pd.read_csv(f"{file_name}", low_memory=False)
    dataset["Label"] = label_encoder.fit_transform(dataset["Label"])
    dataframe = pd.DataFrame(dataset)

    remove_perfect_correlation(dataframe)

    matrix = dataframe.corr()
    plt.title(f"Correlation Matrix : {attack}")
    plt.imshow(matrix, cmap='Blues')
    plt.colorbar()
    plt.show()
    return matrix

def save_correlation_above(matrix, n, filename):
    columns_with_corr_label = []

    # Sélectionner les colonnes ayant une corrélation > n en fonction de "Label"
    for col in matrix.columns:
        if col != 'Label' and (matrix['Label'][col] >= n or matrix['Label'][col] <= -n)and matrix['Label'][col] != 0:
            columns_with_corr_label.append(col)

    # Afficher les colonnes ayant une corrélation > n en fonction de "Label"
    with open(f"data_selection/{filename}", "w") as f:
        f.write(",".join(columns_with_corr_label))

def delete_empty(file_path, files):
    for file in files[:]:
        csv = os.path.join(file_path, file)
        if os.path.getsize(csv) == 0:
            os.remove(csv)
            print(f"Deleted empty file: {file}")
            files.remove(file)

def delete_duplicates(file_path, files):
    files = files[:]
    to_delete = set()
    for i in range(len(files)):
        file1 = files[i]
        path1 = os.path.join(file_path, file1)

        # Skip if file1 is already marked for deletion
        if file1 in to_delete:
            continue

        for j in range(i + 1, len(files)):
            file2 = files[j]
            path2 = os.path.join(file_path, file2)

            # Skip if file2 is already marked for deletion
            if file2 in to_delete:
                continue

            df1 = pd.read_csv(path1)
            df2 = pd.read_csv(path2)

            if df1.equals(df2):
                num1 = int(''.join(filter(str.isdigit, file1)))
                num2 = int(''.join(filter(str.isdigit, file2)))

                # Determine which file to delete (keep the one with the lower number)
                if num1 < num2:
                    to_delete.add(file2)
                    print(f"Marked for deletion: {file2}")
                else:
                    to_delete.add(file1)
                    print(f"Marked for deletion: {file1}")
                    break
    for file in to_delete:
        os.remove(os.path.join(file_path, file))

def clean_dataselect(num):
    csv_files = [f for f in os.listdir("data_selection") if f.startswith(f'{num}') and f.endswith('.csv')]
    file_path = "data_selection"
    delete_empty(file_path, csv_files)
    delete_duplicates(file_path, csv_files)

def frange(start, stop, step):
    while start >= stop:
        yield round(start, 3)
        start += step

def auto_correlation(num):
    print("#===---------------------------------------------------------------------------------------------------===#")
    print(f"auto_correlation {num}")
    matrix = make_matrix(f"clean_dataset/dataset_{num}.csv",f"dataset_{num}")
    for i in list(frange(90, 10, -10)) + list(frange(9, 1, -1)):
        print(i)
        save_correlation_above(matrix, 0, f"{num}00.csv")
        if i % 10 == 0:
            save_correlation_above(matrix, i*0.01, f"{num}{i}.csv")
        else:
            save_correlation_above(matrix, i*0.01, f"{num}0{i}.csv")

    clean_dataselect(num)


def main():
    auto_correlation("0")
    auto_correlation("1")
    auto_correlation("2")
    auto_correlation("3")
    auto_correlation("4")
    auto_correlation("5")
    auto_correlation("6")
    auto_correlation("7")


if __name__ == "__main__":
    main()

