"""
author - cyber
date   - 30/10/26
socket client
"""
import socket
from Bruteforce import Bruteforce
from protocol import *
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080



def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        data = protocol_recive(client_socket).decode()
        password_hasehd, start, end, length = data.split(',')
        start = int(start)
        end = int(end)
        length = int(length)
        print(password_hasehd, start, end, length)
        bruteforce = Bruteforce(password_hasehd, length)
        trying = Bruteforce.find(bruteforce, password_hasehd,(start,end),length)
        if trying is not None:
            print('the password is: ', trying)
        else:
            print('the password is not in this range')




    except socket.error as msg:
        print('error in communication with server - ' + str(msg))
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()