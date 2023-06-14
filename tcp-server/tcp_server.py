import logging
import socket
import threading

import data_collector


class TcpServer:
    def __init__(self, host="", port=6000, timeout=10):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(timeout)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        logging.info(f"Listening on {self.host}:{self.port}")
        # Thread for accepting connections
        conn_thread = threading.Thread(target=self._accept_connections, daemon=True)
        conn_thread.start()

        conn_thread.join()

    def _accept_connections(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_socket.settimeout(10.0)
                logging.info(f"Connected by {client_address}")

                # Thread for receiving input from client
                recv_thread = threading.Thread(target=self._recv_data, args=(client_socket,))
                recv_thread.start()
            except socket.timeout:
                logging.info("no client")

    def _recv_data(self, client_socket):
        device_id = self.read_device_id(client_socket)
        collector = data_collector.DataCollector(device_id)
        while client_socket:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                collector.add_data(data)

            except socket.timeout:
                # No data received from client within timeout period, reset client
                logging.info(f"\n{device_id} - no data received timeout.")
                break
            except ConnectionResetError:
                logging.info("\n{device_id} - Connection with client reset.")
                break
        client_socket.close()
        logging.info(f'{device_id} disconnected\n')

    @staticmethod
    def read_device_id(client_socket):
        if client_socket:
            logging.info("Reading device id...")
            received_data = receive_exact_bytes(client_socket, 8)  # Receive 8 bytes of data
            # Convert received data to the chip ID
            device_id = int.from_bytes(received_data, byteorder='big', signed=False)
            logging.info(f"Device id: {hex(device_id)}\n")
            return hex(device_id)
        return 0

@staticmethod
def receive_exact_bytes(client_socket, num_bytes):
    received_data = b''  # Initialize an empty byte string to store received data

    while len(received_data) < num_bytes:
        remaining_bytes = num_bytes - len(received_data)
        data = client_socket.recv(remaining_bytes)
        if not data:
            # Connection closed prematurely
            break
        received_data += data

    return received_data


# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s - [%(thread)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    server = TcpServer()
    server.start()
