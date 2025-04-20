import time
import random
import subprocess
import os
import datetime
import re
import shutil

import retrieve_requests
import dossier_local.local.analyse_suricata as analyse_suricata
import dossier_local.local.analyse_yara as analyse_yara
import dossier_local.local.analyse_snort as analyse_snort
import dossier_local.online.analyse_VT as analyse_VT
import dossier_local.online.analyse_AbuseIPDB as analyse_AbuseIPDB
import dossier_local.ia.predict as predict

from send_alert import start_client as send_alert
from config import YARA, SNORT, SURICATA,  VIRUS_TOTAL, IPDB, IA, RANDOM_FOREST, SUPPORT_VECTOR_MACHINE

# Print the config
print(YARA, SNORT, SURICATA, VIRUS_TOTAL, IPDB, IA, RANDOM_FOREST, SUPPORT_VECTOR_MACHINE)

# Configuration
ID_ALERT_FILE = "id_alert.txt"
save_dir_alert = "alerts"
os.makedirs(save_dir_alert, exist_ok=True)


def get_daily_id():
    """
    Retrieve et update the ID alert of the day.
    If it is a new day, the ID is reset to 0.
    :return: The new ID of alert.
    """
    today_date = datetime.datetime.now().strftime("%d_%m_%Y")

    # Check if the file exist
    if os.path.exists(ID_ALERT_FILE):
        with open(ID_ALERT_FILE, "r") as file:
            last_date, last_id = file.readline().strip().split(",")

        # If the date is different, we update the ID
        if last_date != today_date:
            current_id = 0
        else:
            current_id = int(last_id) + 1
    else:
        current_id = 0  # First ID of the day

    # Save the new ID ans the date in the file
    with open(ID_ALERT_FILE, "w") as file:
        file.write(f"{today_date},{current_id}")

    return current_id


def rename_pcap(name_alert, methode, filename):
    """
    Rename a PCAP file in the format : id_alert_date_name_alert.pcap
    :param idAlert: Unique identifier of the alert.
    :param nameAlert: Name of the alert.
    :param filename: Path of the PCAP file.
    :return: New path of the rename file.
    """
    id_alert = get_daily_id()

    # Clean the alert name
    if isinstance(name_alert, list):
        name_alert = " ".join(str(word) for word in name_alert)  # Convertir en string proprement
    else:
        name_alert = str(name_alert)
    clean_name_alert = re.sub(r'[^a-zA-Z0-9_-]', '_', name_alert).lower()

    # Get the date of the day (jj_mm_aaaa)
    date_str = datetime.datetime.now().strftime("%d_%m_%Y")

    # Creation of the new name of the file
    new_filename = f"{id_alert}__{date_str}__{methode}__{clean_name_alert}.pcap"

    # Get the original repertory
    directory = os.path.dirname(filename)
    new_filepath = os.path.join(directory, new_filename)

    # Rename the PCAP file
    os.rename(filename, new_filepath)

    return new_filepath

def run():
    while True:

        # ---Get PCAP file---
        filename = retrieve_requests.get_pcap_file()
        if filename == None:
            continue
        print("---------------------")
        # Put the flag to false = no alert detected
        flag = False

        # -----LOCAL AUDIT------
        if YARA == True:
            # ---Yara---
            yara_rules_file = "dossier_local/local/rules/yara-rules-full.yar"
            alert_yara = analyse_yara.analyse_pcap_with_yara(filename, yara_rules_file)

            if alert_yara != False and alert_yara != None:
                # Rename the PCAP file
                new_filename = rename_pcap(alert_yara, "local_yara", filename)

                # Send the file to the server and save it in the directory
                # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                send_alert(new_filename)
                shutil.move(new_filename, save_dir_alert)

                flag = True
                print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                continue

        if SNORT == True:
            # ---Snort---
            rules = analyse_snort.load_snort_rules("dossier_local/local/rules/snort3-community.rules")
            alert_snort = analyse_snort.analyse_pcap_with_snort(filename, rules)

            if alert_snort != False and alert_snort != None:
                print(alert_snort)
                # Rename the PCAP file
                new_filename = rename_pcap(alert_snort, "local_snort", filename)

                # Send the file to the server and save it in the directory
                # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                send_alert(new_filename)
                shutil.move(new_filename, save_dir_alert)

                flag = True
                print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                continue

        if SURICATA == True:
            # ---Suricata---
            alert_suricata = analyse_suricata.analyse_pcap_with_suricata(filename)

            if alert_suricata != False and alert_suricata != None:
                # Rename the PCAP file
                new_filename = rename_pcap(alert_suricata, "local_suricata", filename)

                # Send the file to the server and save it in the directory
                # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                send_alert(new_filename)
                shutil.move(new_filename, save_dir_alert)

                flag = True
                print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                continue

        # -----ONLINE AUDIT------
        if IPDB == True:
            # ---AbuseIPDB---
            alert_abuse = analyse_AbuseIPDB.analyse_pcap_with_abuseIPDB(filename)

            if alert_abuse != False and alert_abuse != None:
                # Rename the PCAP file
                new_filename = rename_pcap(alert_abuse, "online_abuseIPDB", filename)

                # Send the file to the server and save it in the directory
                # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                send_alert(new_filename)
                shutil.move(new_filename, save_dir_alert)

                flag = True
                print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                continue

        if VIRUS_TOTAL == True:
            # ---VirusTotal---
            alert_VT = analyse_VT.analyse_pcap_with_VT(filename)

            if alert_VT != False and alert_VT != None:
                # Rename the PCAP file
                new_filename = rename_pcap(alert_VT, "online_virustotal", filename)

                # Send the file to the server and save it in the directory
                # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                send_alert(new_filename)
                shutil.move(new_filename, save_dir_alert)

                flag = True
                print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                continue

        # -----IA AUDIT-----
        if IA == True:
            # ---Random Forest---
            if RANDOM_FOREST == True:
                try:
                    alert_random = predict.prediction_with_random_forest(filename)
                    if alert_random != False and alert_random != None and alert_random != "DoS attacks-SlowHTTPTest":
                        # Rename the PCAP file
                        new_filename = rename_pcap(alert_random, "ia_random_forest", filename)

                        # Send the file to the server and save it in the directory
                        # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                        send_alert(new_filename)
                        shutil.move(new_filename, save_dir_alert)

                        flag = True
                        print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                        continue
                except Exception as e:
                    pass
                    # print(e)

            # ---Support vector machine---
            if SUPPORT_VECTOR_MACHINE == True:
                try:
                    alert_vector = predict.prediction_with_support_vector_machine(filename)
                    if alert_vector != False and alert_vector != None and alert_vector != "DoS attacks-Hulk" and alert_vector != "DDOS attack-HOIC":
                        print(alert_vector)
                        # Rename the PCAP file
                        new_filename = rename_pcap(alert_vector, "ia_support_vector_machine", filename)

                        # Send the file to the server and save it in the directory
                        # subprocess.run(["sudo","python3", "communication_client.py", new_filename])
                        send_alert(new_filename)
                        shutil.move(new_filename, save_dir_alert)

                        flag = True
                        print(f"Alert detected, file rename : {new_filename}, and save in Alerts.")
                        continue
                except Exception as e:
                    pass
                    # print(e)

        # If no alert detected
        if flag == False:
            os.remove(filename)
            print(f"No alert detected on {filename}")

if __name__ == '__main__':
    run()