import subprocess

import schedule
import time
from get_update import start_client as get_update

# Planifie tous les jours à 3h00
schedule.every().day.at("03:00").do(get_update)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Lancer le planificateur dans un thread séparé
    import threading
    threading.Thread(target=scheduler_loop, daemon=True).start()

    # Exécute immédiatement une première fois
    get_update()
    # Lancer le client principal (blocage ici)
    subprocess.run(["python", "client.py"])
