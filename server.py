"""
author: nir dweck
date: 11/3/22
description: a simple multi-threaded TCP server
"""
import queue
import socket
from os import remove
from threading import Thread
from protocol import *
import hashlib


QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
PASSWORD = '0001739999'
LENGTH = 10
PASWORD_HASEHD = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest().upper()
CLIENTS = []
password_found = False


work_queue = queue.Queue()
for start in range(0, 10000000000, 500000):
    end = start + 500000-1
    work_queue.put((start, end)) #makes a queue of range tuples


def handle_connection(client_socket, client_address):
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
    CLIENTS.append(client_socket)
    thisones_ranges = []
    global password_found
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        # handle the communication
        while not password_found and not work_queue.empty():
            protocol_send(client_socket, f"{PASWORD_HASEHD},{LENGTH}".encode())
            num_of_cores = protocol_recive(client_socket)
            print('num_of_cores:', num_of_cores)
            if not num_of_cores:
                print('client disconnected' + client_address[0] + ':' + str(client_address[1]))
                CLIENTS.remove(client_socket)
                raise ConnectionError
            num_of_cores = int(num_of_cores.decode())
            for i in range(num_of_cores):
                rng = work_queue.get()
                thisones_ranges.append(rng)
                protocol_send(client_socket, str(rng).encode())
            data = protocol_recive(client_socket)
            if not data:
                print('client disconnected' + client_address[0] + ':' + str(client_address[1]))
                CLIENTS.remove(client_socket)
                break
            print(data)
            data = data.decode()
            found,password = data.split(',')
            if found == 'True':
                password_found = True
                for client in CLIENTS:
                    protocol_send(client, b'True,True')
                    print('found')

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        if not password_found:
            for rng in thisones_ranges:
                work_queue.put(rng)
        if client_socket in CLIENTS:
            CLIENTS.remove(client_socket)
        client_socket.close()
        print('in clients:', CLIENTS)


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)
        while True:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection,
                            args=(client_socket, client_address))
            thread.start()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()