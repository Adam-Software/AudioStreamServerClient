import pyaudio
import socket
import wave
import sys

# Socket
HOST = 'localhost'
PORT = 5050

filename = 'temp.wav'

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
INDEX = 0
RECORD_SECONDS = 30

class SocketClientStreamSCard:

    def __init__(self):

        self.file = wave.open(filename, 'rb')

        """ Init audio stream """
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            output = True,
            input = True,
            input_device_index = INDEX,
            frames_per_buffer = CHUNK
        )
        #Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_address = (HOST, PORT)
        self.client_socket.connect(self.socket_address)
        print("Client connected to", self.socket_address)

    def playwav(self):
        # Read data in chunks
        data = self.file.readframes(CHUNK)
        # Play the sound by writing the audio data to the stream
        while data != b'':
            #self.stream.write(data)
            data = self.file.readframes(CHUNK)
            self.client_socket.send(data)

    def playmic(self):
        data = []
        while data != b'':
            data = self.stream.read(CHUNK)
            self.client_socket.send(data)

    def playSCard(self):
        data = []
        while data != b'':
            self.stream.write(data)
            self.client_socket.send(data)


    def close(self):
        """ Graceful shutdown """
        self.client_socket.close()
        self.stream.close()
        self.p.terminate()

# Usage example for pyaudio
a = SocketClientStreamSCard()
#a.playwav()
a.playmic()
a.close()