import socket
import ssl
import os

# Configuration
HOST, PORT = "0.0.0.0", 4433
CERT_FILE = "server_cert.pem"
KEY_FILE = "server_key.pem"
CA_FILE = "ca_cert.pem"
SAVE_DIR = os.path.expanduser("Fichiers_recus")  # Folder where the received files are saved
os.makedirs(SAVE_DIR, exist_ok=True)


# Configuration TLS
def create_ssl_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(CA_FILE)
    context.verify_mode = ssl.CERT_REQUIRED  # Requires a client certificate 
    return context


packet_count = 0

# Function to receive files
def receive_file(conn):
    try:
        while True:
            # Read the name of the file (max size : 256 octets)
            filename_bytes = conn.recv(256)
            if not filename_bytes:
                break  

            global packet_count
            filename = os.path.join(SAVE_DIR, f"alerte_{packet_count}.pcap")
            packet_count += 1

            # Receive and write the file
            with open(filename, "wb") as f:
                while chunk := conn.recv(4096):
                    if not chunk:
                        break
                    f.write(chunk)

            print(f" File saved in {filename}\n")

    except Exception as e:
        print(f" Error in the receive of the file : {e}")


# Function to send a file
def send_file(conn, file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            conn.sendall(f.read())
        print(f" Fichier {file_path} envoyé au client.")
    else:
        print(f"Fichier {file_path} introuvable.")


# Function to start the server
def start_server():
    context = create_ssl_context()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f" Serveur en écoute sur {HOST}:{PORT}...")

    with context.wrap_socket(server_socket, server_side=True) as secure_socket:
        while True :
            conn, addr = secure_socket.accept()
            print(f" Connexion sécurisée depuis {addr}")

            # Receive the file of the client
            receive_file(conn)

            # Send a file to the client
            #send_file(conn, "file_from_server.txt")

            conn.close()

# Execution
if __name__ == "__main__":
    start_server()