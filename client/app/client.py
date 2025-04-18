import hashlib
import json
import socket
import ssl
import os
import argparse

from cryptography import x509
from cryptography.x509 import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes

# Configuration
CLIENT_NAME = os.environ.get('NAME')
SERVER_HOST, SERVER_PORT = "django_app", 4433  # IP du serveur
# SERVER_HOST, SERVER_PORT = "172.20.10.6", 4433  # IP du serveur
CERT_FILE = f"certs/{CLIENT_NAME}_cert.pem"
KEY_FILE = f"certs/{CLIENT_NAME}_key.pem"
CA_FILE = "certs/ca_cert.pem"
CSR_FILE = f"certs/{CLIENT_NAME}.csr"
APP_DIR = "dossier_local"
SAVE_DIR = os.path.expanduser(f"{APP_DIR}/Fichiers_recus")  # Dossier où enregistrer les fichiers reçus
os.makedirs(SAVE_DIR, exist_ok=True)

print(os.path.dirname(os.path.abspath(__file__)), flush=True)


# Function to create the SSL context (TLS)
def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(CA_FILE)
    return context


def generate_key_and_csr():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Sauvegarder la clé privée
    with open(KEY_FILE, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, CLIENT_NAME),
    ])).sign(key, hashes.SHA256())

    with open(CSR_FILE, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    print(f"[✓] CSR générée avec CN = {CLIENT_NAME}")

def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def get_local_hashes(folder_path):
    hashes = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            hashes[relative_path] = compute_sha256(full_path)
    return hashes


def send_csr_and_receive_cert():
    # Connexion non sécurisée temporaire pour l'envoi de la CSR
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        # sock.sendall(b"CSR_REQUEST".ljust(256, b'\0'))  # Type de message
        with open(CSR_FILE, "rb") as f:
            csr_data = f.read()
            sock.sendall(len(csr_data).to_bytes(4, 'big'))
            sock.sendall(csr_data)

        # Réception du certificat signé
        cert_len = int.from_bytes(sock.recv(4), 'big')
        signed_cert = sock.recv(cert_len)

        with open(CERT_FILE, "wb") as f:
            f.write(signed_cert)

        print("[✓] Certificat signé reçu et sauvegardé.")

# Function to send a file to the server
def send_file(conn, file_path):
    if os.path.exists(file_path):
        # Type de communication
        com_type = "ALERT".encode()
        com_type_padded = com_type.ljust(32, b'\0')
        conn.sendall(com_type_padded)

        # Nom du fichier (nom brut, pas le chemin complet)
        filename = os.path.basename(file_path).encode()
        # Envoyer le nom du fichier en 256 octets (paddé si nécessaire)
        filename_padded = filename.ljust(256, b'\0')
        conn.sendall(filename_padded)

        with open(file_path, "rb") as f:
            conn.sendall(f.read())
        print(f" File '{file_path}' send to the server.")
    else:
        print(f" Error : The file '{file_path}' doesn't exist.")


# Function to receive a file
def receive_file(conn):
    received_file_path = os.path.join(SAVE_DIR, "received_from_server.txt")
    with open(received_file_path, "wb") as f:
        while chunk := conn.recv(4096):
            if not chunk:
                break
            f.write(chunk)
    print(f" File received and saved in {received_file_path}")

def get_updated_files(conn):
    # Type de communication
    com_type = "CONNECTION".encode()
    com_type_padded = com_type.ljust(32, b'\0')
    conn.sendall(com_type_padded)
    # 📥 Recevoir les hashes
    length = int.from_bytes(conn.recv(4), "big")
    hashes_json = conn.recv(length)
    server_hashes = json.loads(hashes_json.decode())

    local_hashes = get_local_hashes(APP_DIR)
    to_request = []

    for fname, remote_hash in server_hashes.items():
        local_hash = local_hashes.get(fname)
        if local_hash != remote_hash:
            to_request.append(fname)

    # 📤 Envoyer la liste au serveur
    missing_json = json.dumps(to_request).encode()
    conn.sendall(len(missing_json).to_bytes(4, 'big') + missing_json)

    # 📥 Recevoir les fichiers
    while to_request:
        name_len = int.from_bytes(conn.recv(2), "big")
        filename = conn.recv(name_len).decode()
        data_len = int.from_bytes(conn.recv(4), "big")
        data = conn.recv(data_len)

        full_path = os.path.join(APP_DIR, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(data)

        print(f" ✓ Fichier reçu : {filename}")
        to_request.remove(filename)

# Function to start the client
def start_client(file_to_send):
    if not os.path.exists(CERT_FILE):
        print("[!] Certificat non trouvé. Génération CSR...")
        generate_key_and_csr()
        send_csr_and_receive_cert()

    context = create_ssl_context()

    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER_HOST) as secure_sock:
            print(" Secure connexion established with the server.")

            # Send the file
            # send_file(secure_sock, file_to_send)

            # Receive a file
            # receive_file(secure_sock)

            get_updated_files(secure_sock)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client to send a file to the server by TLS.")
    parser.add_argument("file", help="Path of the file to send")
    args = parser.parse_args()

    start_client(args.file)
