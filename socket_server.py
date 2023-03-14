import socket
import threading


class Server:
    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()

    def __init__(self, addr, port):
        self.sock = None
        self.addr = addr
        self.port = port

        self.client_0 = None
        self.client_1 = None

        self.client_0_thread = None
        self.client_1_thread = None

        self.client_0_key = None
        self.client_1_key = None

    def run(self):
        self.sock.bind((self.addr, self.port))
        self.sock.listen(2)

        self.client_0, _ = self.sock.accept()
        self.client_0_thread = threading.Thread(target=self.client_0_handler)
        self.client_0_thread.start()

        self.client_1, _ = self.sock.accept()
        self.client_1_thread = threading.Thread(target=self.client_1_handler)
        self.client_1_thread.start()

    def client_0_handler(self):
        self.client_0_key = self.client_0.recv(1024)
        print(self.client_0_key)
        while True:
            data = self.client_0.recv(1024)
            if not data:
                break
            self.client_1.send(data)

    def client_1_handler(self):
        self.client_1_key = self.client_1.recv(1024)
        while True:
            data = self.client_1.recv(1024)
            if not data:
                break
            self.client_0.send(data)


if __name__ == '__main__':
    with Server("localhost", 12345) as server:
        server.run()
