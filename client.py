import socket

# server details
PORT = 65432
SERVER = "20.211.33.233"
ADDR = (SERVER, PORT)


# connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
try:
    client.connect(ADDR)
    connected = True
    print("Connected to server..")
except Exception as e:
    print(f"Error!: {str(e)}")


# close the connection
if connected:
    client.close()
    print("Disconnected.")

