"""
author - cyber
date   - 30/10/26
socket client
"""
import queue
import socket
import os
from threading import Thread
from Bruteforce import Bruteforce
from protocol import *
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
NUM_OF_CORES = str(os.cpu_count())

my_chunks = queue.Queue()
results = queue.Queue()
threads = []


def go_bruteforce(password_hashed,length):
    rng = my_chunks.get()
    bruteforce = Bruteforce(password_hashed,length)
    trying = bruteforce.find(password_hashed,rng,length)
    if trying is not None:
        results.put(trying)

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        while True:
            data = protocol_recive(client_socket)
            data = data.decode()
            password_hashed, length = data.split(',')
            if length == 'True':
                break
            length = int(length)
            protocol_send(client_socket, NUM_OF_CORES.encode())
            for i in range(int(NUM_OF_CORES)):
                chunk = protocol_recive(client_socket).decode()
                chunk = chunk.strip("()")
                start, end = chunk.split(',')
                my_chunks.put((int(start), int(end)))
            for i in range(int(NUM_OF_CORES)):
                t = Thread(target=go_bruteforce, args=(password_hashed,length))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            if not results.empty():
                password = results.get()
                answer = f"True,{password}"
            else:
                answer = 'False,False'
            protocol_send(client_socket, answer.encode())




    except socket.error as msg:
        print('error in communication with server - ' + str(msg))
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()