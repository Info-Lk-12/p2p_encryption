from enc_dec import full_encrypt, full_decrypt, public_keys
from keytools import load_private_key


def save_message(file, message):
    with open(file, "wb") as f:
        f.write(message)


def read_message(file):
    with open(file, "rb") as f:
        return f.read()


def main():
    private_key = load_private_key("private_key.pem")
    receiver_keys = public_keys("public_keys")

    encrypt_mode = input("encrypt or decrypt? [E/d] >") in ["E", "e", ""]

    if encrypt_mode:
        message = input("Message >")
        possible_receivers = map(lambda k: k["name"], receiver_keys)
        for i, receiver in enumerate(possible_receivers):
            print(f"{i}: {receiver}")
        receiver = receiver_keys[int(input("Receiver >"))]["key"]

        encrypted_message, signature = full_encrypt(message, private_key, receiver)
        save_message("msg.bin", encrypted_message + b"|||" + signature)
    else:
        encrypted_message, signature = read_message("msg.bin").split(b"|||")
        possible_senders = map(lambda k: k["name"], receiver_keys)
        for i, sender in enumerate(possible_senders):
            print(f"{i}: {sender}")
        sender = receiver_keys[int(input("Receiver >"))]["key"]

        message = full_decrypt(encrypted_message, signature, private_key, sender)
        if message is None:
            print("Message could not be decrypted. Probably the sender is not who he claims to be.")
        else:
            print(message.decode("utf-8"))


if __name__ == '__main__':
    main()
