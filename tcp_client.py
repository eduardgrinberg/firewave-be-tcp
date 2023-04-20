import socket
import wave

# create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
server_address = ('localhost', 6000)
client_socket.connect(server_address)

# open the file and read and send its contents in chunks of 1024 bytes
with wave.open('test.wav', 'rb') as wavefile:
    num_frames = wavefile.getnframes()
    audio_data = wavefile.readframes(num_frames)
    chunk_size = 1024
    offset = 0

    while offset < len(audio_data):
        chunk = audio_data[offset:offset + chunk_size]
        print('Sending Data ' + len(chunk).__str__())
        client_socket.sendall(chunk)
        offset += chunk_size

# close the socket
client_socket.close()