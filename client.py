import socket
import time

server_ip = '127.0.0.1'  # Change this to the server's IP if needed
server_port = 4404

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((server_ip, server_port))
    print("Connected to the server.")

    # Prepare the packet
    packet = '+CMGR: "REC UNREAD","SRVGPRS","","24/12/15,22:09:37+0330"\r\n^Sample string$\r\n'
    
    # Send the packet
    client_socket.send(packet.encode('utf-8'))
    print("Packet sent.")

    # Wait for the ACK from the server
    ack = client_socket.recv(1024).decode('utf-8')
    print("Received ACK from server:", ack)

    # Wait for the second message from the server
    second_message = client_socket.recv(1024).decode('utf-8')
    print("Received second message from server:", second_message)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
 ```python
    # Close the client socket
    client_socket.close()
    print("Connection closed.")
