#!/bin/bash
mkdir -p certs
cd certs

echo "=== Création de la CA (autorité de certification) ==="
openssl req -new -x509 -days 365 -nodes \
    -subj "/C=CA/ST=QC/L=Chicoutimi/O=UQAC/OU=HIDS/CN=ca" \
    -keyout ca_key.pem -out ca_cert.pem

echo "=== Création de la clé du serveur ==="
openssl genrsa -out server_key.pem 2048

echo "=== CSR pour le serveur ==="
openssl req -new -key server_key.pem \
    -subj "/C=CA/ST=QC/L=Chicoutimi/O=UQAC/OU=HIDS/CN=django_app" \
    -out server.csr

echo "=== Signature du certificat serveur par la CA ==="
openssl x509 -req -in server.csr -CA ca_cert.pem -CAkey ca_key.pem \
    -CAcreateserial -out server_cert.pem -days 365

echo "=== Création de la clé du client ==="
openssl genrsa -out client1_key.pem 2048

echo "=== CSR pour le client ==="
openssl req -new -key client1_key.pem \
    -subj "/C=CA/ST=QC/L=Chicoutimi/O=UQAC/OU=HIDS/CN=client1" \
    -out client1.csr

echo "=== Signature du certificat client par la CA ==="
openssl x509 -req -in client1.csr -CA ca_cert.pem -CAkey ca_key.pem \
    -CAcreateserial -out client1_cert.pem -days 365

echo "=== Création de la clé du client ==="
openssl genrsa -out client2_key.pem 2048

echo "=== CSR pour le client ==="
openssl req -new -key client2_key.pem \
    -subj "/C=CA/ST=QC/L=Chicoutimi/O=UQAC/OU=HIDS/CN=client2" \
    -out client2.csr

echo "=== Signature du certificat client par la CA ==="
openssl x509 -req -in client2.csr -CA ca_cert.pem -CAkey ca_key.pem \
    -CAcreateserial -out client2_cert.pem -days 365

echo "=== Nettoyage ==="
rm *.csr *.srl

echo "✅ Certificats générés dans certs/"
