from logging import raiseExceptions
import socket

# Constants
FORMAT = "utf-8"

# server details
PORT = 65432
SERVER = "20.211.33.233"
ADDR = (SERVER, PORT)


# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)
    print("Connected to server..")
except Exception as e:
    print(f"Error! See exception below")
    raise Exception(e)


# Test 1 data cycle
data = client.recv(1024).decode(FORMAT).strip("\n")
print(data)
x = input()
msg = x + "\n"
client.send(bytes(msg, "UTF-8"))
data = client.recv(1024).decode(FORMAT).strip("\n")
print(data)


# close the connection
client.close()
print("Disconnected.")

