from enc_dec import full_encrypt, full_decrypt
from keytools import load_private_key, load_public_key

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import socket
import threading


def export_key(key):
    return key.public_bytes(encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo)


def import_key(key):
    return serialization.load_pem_public_key(key, backend=default_backend())


def receiver(conn, private_key, other_public_key):
    while True:
        enc_data = conn.recv(1024)
        if not enc_data:
            break

        enc_data, sig = enc_data.split(b"|||")
        data = full_decrypt(enc_data, sig, private_key, other_public_key)
        print("\n" + data.decode("utf-8"))


def main(addr, port):
    private_key = load_private_key("private_key.pem")
    public_key = load_public_key("public_key.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((addr, port))

        sock.listen(1)
        conn, usr = sock.accept()
        print("Connected")

        conn.sendall(export_key(public_key))
        print("Sent public key")

        other_public_key = import_key(conn.recv(1024))
        print("Received public key")

        receiver_thread = threading.Thread(target=receiver, args=(conn, private_key, other_public_key,))
        receiver_thread.start()

        while True:
            try:
                data = input("\nMessage >")
                if data == "exit":
                    break

                enc_data, sig = full_encrypt(data, private_key, other_public_key)
                conn.sendto(enc_data + b"|||" + sig, usr)
            except KeyboardInterrupt:
                conn.close()
                break


if __name__ == '__main__':
    main(
        input("Address >"),
        int(input("Port >"))
    )
