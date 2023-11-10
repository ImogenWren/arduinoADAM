'''

'''

import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192         # The port used by the server

SERVER_ADDRESS = '127.0.0.1:8192'

BUFFER_SIZE = 1024

def json_message(direction):
    local_ip = socket.gethostbyname(socket.gethostname())
    data = {
        'sender': local_ip,
        'instruction': direction
    }
    json_data = json.dumps(data, sort_keys=False, indent=2)
    print("data %s" % json_data)
    send_message(json_data + ";")
    return json_data

def json_command():
    local_ip = socket.gethostbyname(socket.gethostname())
    json_data = listen_message()
    json_data = json.dumps(json_data, sort_keys=False, indent=2)
    print("data %s" % json_data)
    return json_data


def send_message(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data.encode())
        data = s.recv(1024)
    print('Received', repr(data))

def listen_message():
    data = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.listen()
        while 1: # Accept connections from multiple clients
            print('Listening for Server Commands...')
            conn, addr = s.accept()
            print('Connection address:', addr)
            while 1: # Accept multiple messages from each client
                buffer = conn.recv(BUFFER_SIZE)
                buffer = buffer.decode()
                if buffer == ";":
                    conn.close()
                    print("Received all the data")
                    for x in data:
                        print(x)
                        return data
                    break
                elif buffer:
                    print("received data: ", buffer)
                    data.append(buffer)
                else:
                    break

#json_message("SOME_DIRECTION")

listen_message()