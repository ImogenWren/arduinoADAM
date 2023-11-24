# echo-client.py

import socket
import time
import acUnitGlobals as glbs

parse = glbs.jsonParse
pack = glbs.jsonPack


#HOST = "127.0.0.1"  # The server's hostname or IP address
TESTHOST = "10.42.0.1"
HOST = TESTHOST
PORT = 65432  # The port used by the server

json_delay = 1   ## time between json messages to server


def websocketClient():
    try:
        while (1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((HOST, PORT))
                    print(f"Connected to {s}")
                    init_time = time.time()
                    while(1):
                        #if time.time() - init_time >= json_delay:
                            #print("Sending JSON reply")
                            #json_message = pack.dump_json()
                            #s.sendall(json_message.encode("UTF-8"))
                            #init_time = time.time()
                        data = s.recv(1024)
                        print(f"Received {data!r}")
                        error = parse.parse_json(data)
                        if not error:
                            print("JSON Message Parsed - Queue Updated")
                            print(f"output queue: {glbs.set_outputs_queue}")
                            glbs.command_received = True
                            success_code = "0"
                            s.sendall(success_code.encode("UTF-8"))
                        else:
                            print(f"JSON Parsing Error, code: {error}")
                            error = str(error)
                            s.sendall(error.encode("UTF-8"))  ## error must always be int here?
                except ConnectionError:
                    print("Caught Connection Error, restarting")
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    except Exception as ex:
        glbs.generic_exception_handler(ex)
        raise

        #time.sleep(5)


if __name__ == '__main__':
    websocketClient()