"""
author: nir dweck
date: 11/3/22
description: a simple multi-threaded TCP server
"""
import queue
import socket
from threading import Thread
from protocol import *
import hashlib


QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080
PASSWORD = '0002139999'
LENGTH = 10
PASWORD_HASEHD = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest().upper()
CLIENTS = []

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
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        # handle the communication

        thisones_range = work_queue.get()
        start_rng, end_rng = thisones_range
        data = f"{PASWORD_HASEHD},{start_rng},{end_rng}, {LENGTH}".encode()
        protocol_send(client_socket, data)
        while True:
            data = protocol_recive(client_socket)
            if not data:
                print('client disconnected' + client_address[0] + ':' + str(client_address[1]))
                CLIENTS.remove(client_socket)
                # need to make to save what the client worked on
                #^- protocol will be password,range of work as data tuple
                break
            if data == ('password is: ' + PASWORD_HASEHD).encode():
                for client in CLIENTS:
                    if client != client_socket:
                        protocol_send(client_socket, b'True')

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        client_socket.close()


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