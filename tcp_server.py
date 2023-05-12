import socket
import threading
import data_collector
import logging


class TcpServer:
    def __init__(self, host="", port=6000, timeout=1):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(timeout)
        self.client_socket = None
        self.data_collector = data_collector.DataCollector()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Listening on {self.host}:{self.port}")
        # Thread for accepting connections
        conn_thread = threading.Thread(target=self._accept_connections, daemon=True)
        conn_thread.start()

        # Thread for receiving input from client
        recv_thread = threading.Thread(target=self._recv_data, daemon=True)
        recv_thread.start()

        conn_thread.join()
        recv_thread.join()

    def _accept_connections(self):
        while True:
            try:
                if not self.client_socket:
                    self.client_socket, client_address = self.server_socket.accept()
                    self.client_socket.settimeout(10.0)
                    print(f"Connected by {client_address}")
            except socket.timeout:
                logging.info("no client")

    def _recv_data(self):
        while True:
            if self.client_socket:  # find function to see if there is incoming data
                try:
                    data = self.client_socket.recv(1024)
                    if not data:
                        break
                    self.data_collector.add_data(data)

                except socket.timeout:
                    # No data received from client within timeout period, reset client
                    self.client_socket = None
                    logging.info("\nno data received timeout.")
                except ConnectionResetError:
                    logging.info("\nConnection with client reset.")
                    self.client_socket = None


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    server = TcpServer()
    server.start()
