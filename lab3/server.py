#!/usr/bin/env python

import socket
import signal
import random

class GuessServer:
    def __init__(self, port):
        self.port       = port
        self.chunk_size = 1024
        self.running    = True


    def stopper(self, sig, frame):
        self.running = False
        socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ).connect( ('localhost', self.port) )
    
    def run(self):
        target_number = 100
        attempts = 0
        while self.running:
            print('Opening socket')
            num = 0
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # self.socket = s
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(("0.0.0.0", self.port))
                    print('binded')
                    s.listen()
                    print('listened')
                    conn, addr = s.accept()
                    print('accepted')
                    print('Opened socket')
                    with conn:
                        print(f"Connected by {addr}")
                        while self.running:
                            try:
                                data = conn.recv(self.chunk_size)
                                data = data.decode('utf-8')
                                print(data)
                                cmd = data.split(' ')
                                response = ' '
                                cmd[0] = cmd[0].upper().strip()
                                if cmd[0] == 'STOP':
                                    self.running = False
                                    response = 'EXIT'
                                elif cmd[0] == 'NEW':
                                    if attempts > 0:
                                        response = f'Last game took {str(attempts)} attempts'
                                    target_number = random.randint(0, 1000)
                                    #print(target_number)
                                    attempts = 0
                                elif cmd[0] == 'GUESS':
                                    if len(cmd) > 1:
                                        attempts += 1
                                        try:
                                            num = int(cmd[1])
                                            if num == target_number:
                                                response = 'EQUAL'
                                                #target_number = -target_number
                                            elif num < target_number: 
                                                response = 'LESS'
                                            elif num > target_number:
                                                response = 'MORE'
                                        except Exception as e:
                                            reponse = 'Malformed command'

                                conn.sendall(response.encode('utf-8'))
                            except Exception as e:
                                print(e)
                            if not data:
                                break
                            num += 1 

            except Exception as e:
                print(e)


if __name__ == '__main__':
    guess_server = GuessServer(5005)
    signal.signal(signal.SIGINT, guess_server.stopper)
    guess_server.run()
