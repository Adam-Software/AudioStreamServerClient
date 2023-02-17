import socket
import pyaudio

# Socket
HOST = 'localhost'
PORT = 5010

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
BUFF_SIZE = 65000

class SocketClient:

    def __init__(self):
        """ Init audio stream """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            output=True,
            input=True,
            frames_per_buffer = CHUNK
        )

        #Connect to UDP server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.client_socket.bind((HOST, (PORT)))

    def getmic(self):
        #Send msg
        message = b'Hello'
        self.client_socket.sendto(message, (HOST, PORT-1))
        print("Client connected to", (HOST, PORT-1))

        data = []
        while data != b'':
            data = self.stream.read(CHUNK)
            self.client_socket.sendto(data, (HOST, PORT-1))

    def play(self):
        message = b'Hello'
        self.client_socket.sendto(message, (HOST, PORT-1))
        print("Client connected to", (HOST, PORT))

        packet = []
        while packet != b'':
            packet, _ = self.client_socket.recvfrom(BUFF_SIZE)
            self.stream.write(packet)

    def close(self):
        """ Graceful shutdown """
        self.client_socket.close()
        self.stream.close()
        self.p.terminate()
        print("Client closed")

a = SocketClient()
#a.getmic()
a.play()

