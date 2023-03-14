import os
from hashlib import md5

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from keytools import load_public_key


general_padding = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)
sign_padding = padding.PSS(
    mgf=padding.MGF1(hashes.SHA256()),
    salt_length=padding.PSS.MAX_LENGTH
)


def full_encrypt(message, private_key, other_public_key):
    cipher = other_public_key.encrypt(message.encode("utf-8"), general_padding)
    signature = private_key.sign(cipher, sign_padding, hashes.SHA256())

    return cipher, signature


def full_decrypt(encrypted_message, signature, private_key, public_key):
    try:
        public_key.verify(signature, encrypted_message, sign_padding, hashes.SHA256())
    except InvalidSignature:
        return None

    return private_key.decrypt(encrypted_message, general_padding)


def public_keys(folder):
    out = list()
    for key in os.listdir(folder):
        if key.endswith('.pem'):
            out.append({"name": key, "key": load_public_key(os.path.join(folder, key))})
    
    return out


def find_key_holder(key, folder):
    for key_holder, public_key in public_keys(folder):
        if md5(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                       format=serialization.PublicFormat.SubjectPublicKeyInfo)).hexdigest() == md5(key).hexdigest():
            return key_holder

    return None
