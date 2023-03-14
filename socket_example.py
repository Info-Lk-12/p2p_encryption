from enc_dec import full_encrypt, full_decrypt, public_keys
from keytools import load_private_key, load_public_key

from cryptography.hazmat.primitives import serialization

import socket


addr = input("Address >")
port = int(input("Port >"))
name = input("Name >")


def export_key(key):
    return key.public_bytes(encoding=serialization.Encoding.PEM,
                            format=serialization.PublicFormat.SubjectPublicKeyInfo)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((addr, port))
    print("Connected")

    private_key = load_private_key("private_key.pem")
    public_key = load_public_key("public_key.pem")
    receiver_keys = public_keys("public_keys")

    sock.send(name.encode("utf-8"))
    sock.send(export_key(public_key))
