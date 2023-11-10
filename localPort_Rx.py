'''
 Sending and Receiving JSON messages over internal port using websockets

 Method found @:
 https://stackoverflow.com/questions/53348412/sending-json-object-to-a-tcp-listener-port-in-use-python

'''


import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192         # The port used by the server
BUFFER_SIZE = 512

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

server_socket()