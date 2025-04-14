import socket
import ssl
import os
import django
from django.core.files.base import File

# Initialisation de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HIDS.settings')  # Remplace par ton module de settings
django.setup()

from api.models import Alert, Agent


# Configuration
HOST, PORT = "127.0.0.1", 4433
CERT_FILE = "certs/server_cert.pem"
KEY_FILE = "certs/server_key.pem"
CA_FILE = "certs/ca_cert.pem"
SAVE_DIR = os.path.expanduser("Fichiers_recus")  # Folder where the received files are saved
os.makedirs(SAVE_DIR, exist_ok=True)

print(os.path.dirname(os.path.abspath(__file__)), flush=True)


# Configuration TLS
def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(CA_FILE)
    context.verify_mode = ssl.CERT_REQUIRED  # Requires a client certificate
    return context


packet_count = 0

# TODO : Utiliser l'ip source pour get l'agent
# Add the alerts to the database
def add_in_database(file_path):
    filename = os.path.basename(file_path)
    parts = filename.split("_")

    alert_source = parts[0]
    alert_type = parts[1]
    alert_description = f"Alerte détectée de type '{alert_type}' par '{alert_source}'"
    alert_level = 3 if alert_type.lower() == "DDOS" else 1

    agent = Agent.objects.filter(id=1).first()
    if not agent:
        print(f"Agent not found with IP 1")
        return
    with open(file_path, 'rb') as f:
        alert = Alert.objects.create(
            agent=agent,
            source=alert_source,
            type=alert_type,
            description=alert_description,
            level=alert_level,
            pcap=File(f, name=filename)
        )
        alert.save()
        print(f"[✓] Alerte enregistrée avec succès (ID {alert.id}) pour l'agent {agent.name}")
    # Supprimer le fichier après l'ajout dans la base de données
    try:
        os.remove(file_path)
        print(f"[🗑] Fichier supprimé : {file_path}")
    except Exception as e:
        print(f"[!] Erreur lors de la suppression du fichier : {e}")

# Function to receive files
def receive_file(conn):
    try:
        while True:
            # Read the name of the file (max size : 256 octets)
            filename_padded = conn.recv(256)
            if not filename_padded:
                break
            filename = filename_padded.rstrip(b'\0').decode()

            if "\x00" in filename:
                print("[!] Nom de fichier invalide (caractère nul) {}|".format(filename))
                indices = [i for i, c in enumerate(filename) if c == '\x00']
                print(f"Indices des caractères nuls : {indices}")
                return

            global packet_count
            # filename = os.path.join(SAVE_DIR, f"alerte_{packet_count}.pcap")
            filename = os.path.join(SAVE_DIR, filename)
            if "\x00" in filename:
                print("[!] Nom de fichier invalide (caractère nul) : {}|".format(filename))
                # return
            packet_count += 1

            # Receive and write the file
            with open(filename, "wb") as f:
                while chunk := conn.recv(4096):
                    if not chunk:
                        break
                    f.write(chunk)

            print(f" File saved in {filename}", flush=True)
            add_in_database(filename)

    except Exception as e:
        print(f" Error in the receive of the file : {e}", flush=True)


# Function to send a file
def send_file(conn, file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            conn.sendall(f.read())
        print(f" Fichier {file_path} envoyé au client.", flush=True)
    else:
        print(f"Fichier {file_path} introuvable.")


# Function to start the server
def start_server():
    context = create_ssl_context()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f" Serveur en écoute sur {HOST}:{PORT}...", flush=True)

    with context.wrap_socket(server_socket, server_side=True) as secure_socket:
        while True :
            conn, addr = secure_socket.accept()
            print(f" Connexion sécurisée depuis {addr}", flush=True)

            # Receive the file of the client
            receive_file(conn)

            # Send a file to the client
            #send_file(conn, "file_from_server.txt")

            conn.close()

# Execution
if __name__ == "__main__":
    start_server()
