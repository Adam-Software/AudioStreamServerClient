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

class SocketServerStreamSCard():

    def __init__(self):
        """ Init audio stream """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            output=True,
            input=True,
            frames_per_buffer=CHUNK
        )
        #Start UDP Server
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        self.server_socket.bind((HOST, (PORT-1)))

        print('server listening at', (HOST, PORT-1))

    def play(self):
        msg, client_addr = self.server_socket.recvfrom(BUFF_SIZE)
        print('[GOT connection from]... ', client_addr, msg)

        frame, _ = self.server_socket.recvfrom(BUFF_SIZE)
        while frame != b'':
            frame, _ = self.server_socket.recvfrom(BUFF_SIZE)
            self.stream.write(frame)

    def getmic(self):
        msg, client_addr = self.server_socket.recvfrom(BUFF_SIZE)
        print('[GOT connection from]... ', client_addr, msg)

        data = []
        while data != b'':
            data = self.stream.read(CHUNK)
            self.server_socket.sendto(data, (HOST, PORT))

    def close(self):
        """ Graceful shutdown """
        self.server_socket.close()
        self.stream.close()
        self.p.terminate()
        print("Server closed")


# Usage example for pyaudio
a = SocketServerStreamSCard()
#a.play()
a.getmic()




