import hashlib
import json
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
HOST, PORT = "django_app", 4433
CERT_FILE = "certs/server_cert.pem"
KEY_FILE = "certs/server_key.pem"
CA_FILE = "certs/ca_cert.pem"
CA_KEY_FILE = "certs/ca_key.pem"
SAVE_DIR = os.path.expanduser("Fichiers_recus")  # Folder where the received files are saved
os.makedirs(SAVE_DIR, exist_ok=True)


from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

def extract_cn_from_csr(csr_data):
    csr = x509.load_pem_x509_csr(csr_data, default_backend())
    cn = csr.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    return cn

def signer_csr(csr_pem_path, ip, ca_cert_path = CA_FILE, ca_key_path = CA_KEY_FILE):
    # Charger la CSR
    with open(csr_pem_path, "rb") as f:
        csr = x509.load_pem_x509_csr(f.read(), default_backend())

    # Charger le certificat de l'autorité
    with open(ca_cert_path, "rb") as f:
        ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())

    # Charger la clé privée de l'autorité
    with open(ca_key_path, "rb") as f:
        ca_key = serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )

    # Créer le certificat signé
    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True
        )
        .sign(private_key=ca_key, algorithm=hashes.SHA256(), backend=default_backend())
    )

    certificate_pem = cert.public_bytes(encoding=serialization.Encoding.PEM).decode()

    agent = Agent.objects.create(
        name=cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value,
        common_name=cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value,
        system="Linux",
        addresse=ip,
        down=False,
        certificate=certificate_pem,
    )

    print(f"[✓] Certificat signé et enregistré dans {agent.id}")

    return certificate_pem

def handle_cert_request(conn):
    try:
        # 1. Recevoir la CSR du client (demande de certificat)
        csr_length = int.from_bytes(conn.recv(4), "big")
        csr_data = conn.recv(csr_length)

        if not csr_data:
            print("[!] Aucun CSR reçu.")
            return

        print("[✓] CSR reçu.")

        # 2. Signer le CSR et obtenir le certificat signé
        signed_cert = signer_csr(csr_data)

        # 3. Renvoyer le certificat signé au client
        cert_length = len(signed_cert).to_bytes(4, "big")
        conn.sendall(cert_length + signed_cert.encode())

        print("[✓] Certificat signé renvoyé au client.")

    except Exception as e:
        print(f"[!] Erreur lors du traitement de la demande de certificat : {e}")

# Configuration TLS
def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(CA_FILE)
    context.verify_mode = ssl.CERT_OPTIONAL
    return context

packet_count = 0

# Add the alerts to the database
def add_in_database(file_path, agent):
    filename = os.path.basename(file_path)
    parts = filename.split("_")

    alert_source = parts[0]
    alert_type = parts[1]
    alert_description = f"Alerte détectée de type '{alert_type}' par '{alert_source}'"
    alert_level = 3 if alert_type.lower() == "DDOS" else 1

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
def receive_alert(conn, agent):
    try:
        while True:
            # Read the name of the file (max size : 256 octets)
            filename_padded = conn.recv(32)
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

            add_in_database(filename, agent)

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

def read_padded(conn, size):
    padded = conn.recv(size)
    if not padded:
        return None
    return padded.rstrip(b'\0').decode()

def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def get_file_hashes(folder_path):
    hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            hashes[relative_path] = compute_sha256(full_path)
    return hashes

def check_update(conn):
    folder = "dossier_partage"
    file_hashes = get_file_hashes(folder)
    hashes_json = json.dumps(file_hashes).encode()
    conn.sendall(len(hashes_json).to_bytes(4, "big") + hashes_json)

    length = int.from_bytes(conn.recv(4), "big")
    missing_json = conn.recv(length)
    missing_files = json.loads(missing_json.decode())

    print(" Fichiers demandés :", missing_files, flush=True)

    for filename in missing_files:
        full_path = os.path.join(folder, filename)
        with open(full_path, "rb") as f:
            data = f.read()
            conn.sendall(len(filename.encode()).to_bytes(2, 'big') + filename.encode())
            conn.sendall(len(data).to_bytes(4, 'big') + data)


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
            try:
                cert_info = conn.getpeercert()
                if not cert_info:
                    # 5. Si le client ne présente pas de certificat, envoyer une demande de certificat

                    print("[*] Aucun certificat reçu, demande de certificat.")
                    handle_cert_request(conn)

                else:
                    subject = dict(x[0] for x in cert_info['subject'])
                    cn = subject.get('commonName')
                    agent = Agent.objects.get(common_name=cn)
                    print(f" Agent : {agent.name}", flush=True)
                    if agent:
                        # Get the message type (max size : 256 octets)
                        com_type = conn.recv(256)
                        print("com_type :", com_type, flush=True)
                        if com_type:
                            com_type = com_type.rstrip(b'\0').decode()
                            if com_type == "ALERT":
                                # Receive the file of the client
                                receive_alert(conn, agent)
                            if com_type == "CONNECTION":
                                agent.adresse = addr[0]
                                agent.save()
                                print(f" Agent : {agent.name}, ip updated", flush=True)
                                check_update(conn)

            # Send a file to the client
                #send_file(conn, "file_from_server.txt")
            except Exception as e:
                print(f" Erreur : {e}")
            finally:
                conn.close()

# Execution
if __name__ == "__main__":
    start_server()
