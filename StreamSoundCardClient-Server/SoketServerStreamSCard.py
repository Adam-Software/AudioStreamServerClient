import pyaudio
import socket
import wave
import sys

# Socket
HOST = 'localhost'
PORT = 5050
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

class SocketServerStreamSCard:

    def __init__(self):
        """ Init audio stream """

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            output = True
        )
        #Start Server
        self.server_socket = socket.socket()
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()
        print('server listening at', (HOST, PORT))


    def play(self):
        """ Play recved file """
        self.client_socket, addr = self.server_socket.accept()
        data = self.client_socket.recv(4096)
        while data != b'':
            try:
                data = self.client_socket.recv(4096)
                self.stream.write(data)
            except:
                print("Client Disconnected")
                continue

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()
        print('close')

# Usage example for pyaudio
def main():
    a = SocketServerStreamSCard()
    while 1:
        a.play()

main()