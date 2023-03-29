import socket 
import signal
import sys
import pyaudio
# import wave

continue_recording = True 
    # sys.exit(0)
# print('Press Ctrl+C')
# signal.pause()

class NumberGuesser:
    def signal_handler(self, sig, frame):
        print('Termination signal received')
        # global continue_recording
        self.running = False

    def __init__(self, addr, port, size = 16000):
        self.addr = addr
        self.port = port
        self.size = size
        self.running = True

    def io_loop(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        chunk = 1024 
        # RECORD_SECONDS = 5
        # WAVE_OUTPUT_FILENAME = "output.wav"

        print(self.addr, self.port)

        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.addr, self.port))
        except Exception as e:
            sock = None
            print('ERROR:', e)

        # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        chunk_counter = 0
        if sock:
            while self.running:
                data = None
                print('> ', end = '', flush = True)
                try:
                    data = input()
                except EOFError:
                    self.running = False

                if data:
                    data = data.encode('utf-8')
                    sock.sendall(data)
                    data = sock.recv(chunk).decode('utf-8')
                    if data in ['LESS', 'MORE', 'EQUAL']:
                        print(f'Your guess is {data}')
                    else:
                        print(data)
                    if data == 'EXIT':
                        self.running = False
        else:
            print('[E] Please check if the server is alive')

        
if __name__ == '__main__':
    # signal.signal(signal.SIGINT, signal_handler)
    addr = sys.argv[1]
    micro_recorder = NumberGuesser(addr, port = 5005)
    micro_recorder.io_loop()
    print()
