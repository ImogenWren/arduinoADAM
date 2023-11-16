'''
 Broadcast Server

 Test server for websockets. Broadcast a JSON command every 5-10 seconds no response required (yet)
https://realpython.com/python-sockets/
'''


# broadcastServer.py


import socket
import time
import acUnitGlobals as glbs
pack = glbs.jsonPack

HOST = "127.0.0.1"
PORT = 65432

TEST_COMMAND = '{"cmd":"set", "V1":"open"}'



print(f"Starting Broadcast Server:\nListening on {HOST}:{PORT}")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while (1):
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            iteration = 0
            while True:
                print(iteration)
                json_command = TEST_COMMAND.encode("UTF-8")
                conn.sendall(json_command)
                data = conn.recv(2048)
                data_dic = pack.unpack_json(data)
                json_print = pack.dump_json()
                #print(data_dic)
                if not data:
                    break
                iteration += 1
                time.sleep(1)


