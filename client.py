import socket
from PIL import Image
from io import BytesIO

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


from state_rep import StateRep

# initialise the state representation object
sr = StateRep(max_iter=1000)

data = client.recv(1024).decode(FORMAT).strip("\n")
next_state = data
print(f"Server: {next_state}")

# Loop / Msg Cycles
while True:

    curr_state = next_state
    # Update nodes in StateRep
    sr.update_nodes(curr_state)

    # get message
    msg = sr.get_message_to_send(curr_state)

    # send message
    client.send(bytes(msg, FORMAT))
    print(f"Client: {msg[0]}")

    # Receive message
    next_state = client.recv(1024).decode(FORMAT).strip("\n")
    print(f"Server: {next_state}")

    # Edge case: Handle Z to A transition
    if len(next_state) > 1 and next_state[0] == "Z":
        next_state = "Z"
        sr.update_edge(curr_state, next_state)

        curr_state = next_state
        sr.update_nodes(curr_state)
        next_state = "A"

    # Update edge
    sr.update_edge(curr_state, next_state)

    # Check if status done
    if sr.status_done():
        break


# close the connection
client.close()
print("Disconnected.")

# Metrics
print(sr.nodes)
print(f"Same Path Traversal count {sr.same_path_traversal}")
print(f"Total count {sr.count}")
print(f"Total edges {sr.total_edges}")

# Display image
Image.open(BytesIO(sr.G.create_png())).show()
