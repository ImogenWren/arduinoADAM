'''
 Sending and Receiving JSON messages over internal port using websockets

 Method found @:
 https://stackoverflow.com/questions/53348412/sending-json-object-to-a-tcp-listener-port-in-use-python

https://realpython.com/python-sockets/

'''


import socket
import json
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
#HOST = "192.168.56.1"
PORT = 8192         # The port used by the server
BUFFER_SIZE = 512

test_command = '{"cmd":"set","V1":"open"}'

def server_socket():
    data = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen()
        while 1: # Accept connections from multiple clients
            print('Listening for client...')
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
                    break
                elif buffer:
                    print("received data: ", buffer)
                    data.append(buffer)
                else:
                    break


def command_server():
    response = []
    iteration = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.connect((HOST, PORT))
        while(1):
            json_message(test_command, s)
            print(f"Iteration: {iteration}\n")
            iteration += 1
            time.sleep(5)








def json_message(direction, soc):
    local_ip = socket.gethostbyname(socket.gethostname())
    data = {
        'sender': local_ip,
        'instruction': direction
    }
    json_data = json.dumps(data, sort_keys=False, indent=2)
    print("data %s" % json_data)
    response = send_message(json_data + ";", soc)
    return response

def send_message(data, soc):
    #soc.connect((HOST, PORT))
    soc.sendall(data.encode())
    response = soc.recv(1024)
    print('Received', repr(data))
    return response




#server_socket()

command_server()