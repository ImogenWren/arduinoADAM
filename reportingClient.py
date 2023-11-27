#

'''
Reporting Client

Sends JSON formatted data messages every X seconds

'''
#https://realpython.com/python-sockets/


import socket
import time
import acUnitGlobals as glbs

parse = glbs.jsonParse
pack = glbs.jsonPack


#HOST = "127.0.0.1"  # The server's hostname or IP address
TESTHOST = "10.42.0.1"
HOST = TESTHOST
PORT = 65433  # The port used by the server

json_delay = 1   ## time between json messages to server
connection_error = 0

def reportingClient():
    global connection_error
    try:
        while (1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect((HOST, PORT))
                    print(f"Connected to {s}")
                    glbs.logging.info(f"websocketClient: Connected to Server: {s}")
                    connection_error = 0
                    init_time = time.time()
                    while(1):
                        elapsed_time = time.time() - init_time
                        print(f"reportingClient: init_time={init_time}, Time.time = {time.time()}, diff={elapsed_time}")
                        if elapsed_time >= json_delay:
                            print("reportingClient: Sending JSON reply")
                            json_message = pack.dump_json()
                            s.sendall(json_message.encode("UTF-8"))
                            init_time = time.time()
                            data = s.recv(1024)
                            print(data)
                        time.sleep(1)
                except ConnectionError:
                    print(f"reportingClient: Caught Connection Error, number since last connect: {connection_error}")
                    if connection_error > 1:  ## prevent this being written to log over and over
                        print("reportingClient: logging exception as first instance")
                        glbs.logging.exception(f"reportingClient: Caught Connection Error, restarting")
                    connection_error += 1
    except KeyboardInterrupt:
        print("reportingClient: Caught keyboard interrupt, exiting")
    except Exception as ex:
        glbs.generic_exception_handler(ex, "reportingClient")
        raise

        #time.sleep(5)


if __name__ == '__main__':
    reportingClient()