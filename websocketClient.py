# echo-client.py

import socket
import time
import acUnitGlobals as glbs

pack = glbs.jsonPack

HOST = "127.0.0.1"  # The server's hostname or IP address
TESTHOST = "10.42.0.1"
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while(1):
        json_message = pack.dump_json()
        s.sendall(json_message.encode("UTF-8"))
        data = s.recv(1024)
        print(f"Received {data!r}")
        time.sleep(5)
