import socket
import ssl
import os
import argparse

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

# Function to create the SSL context (TLS)
def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(CA_FILE)
    return context

# Function to send a file to the server
def send_file(conn, file_path):
    if os.path.exists(file_path):
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

def send_alert(conn, file_path):
    # Type de communication
    com_type = "ALERT".encode()
    com_type_padded = com_type.ljust(32, b'\0')
    conn.sendall(com_type_padded)
    # Send the file
    send_file(conn, file_path)

# Function to start the client
def start_client(file_to_send):
    context = create_ssl_context()

    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        # with context.wrap_socket(sock, server_hostname=SERVER_HOST) as secure_sock:
        #     print(" Secure connexion established with the server.")
        #     get_updated_files(secure_sock)

        with context.wrap_socket(sock, server_hostname=SERVER_HOST) as secure_sock:
            print(" Secure connexion established with the server.")
            # Send an alert
            send_alert(secure_sock, file_to_send)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client to send a file to the server by TLS.")
    parser.add_argument("file", help="Path of the file to send")
    args = parser.parse_args()

    start_client(args.file)