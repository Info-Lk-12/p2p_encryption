import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def load_private_key(path):
    with open(path, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

    return private_key


def load_public_key(path):
    with open(path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    return public_key


if __name__ == '__main__':
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes

    general_padding = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
    sign_padding = padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    )

    private_key, public_key = load_private_key('private_key.pem'), load_public_key('public_key.pem')
    other_public_key = load_public_key('public_keys/famijoku.pem')

    msg = "test"

    encrypted = other_public_key.encrypt(msg.encode("utf-8"), general_padding)
    signed = private_key.sign(encrypted, sign_padding, hashes.SHA256())

    print(signed)
    print(public_key.verify(signed, encrypted, sign_padding, hashes.SHA256()))
