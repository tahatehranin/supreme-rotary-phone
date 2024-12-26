import socket
import threading
import time

ip = '0.0.0.0'  # Listen on all interfaces
port = 4404
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.bind((ip, port))
tcpSocket.listen(5)

print("Server is listening on port", port)

# List of allowed IPs (if needed)
allowed_ips = ['127.0.0.1', '192.168.1.2']

# Different messages for each client based on IP
messages = {
    '127.0.0.1': [b"Hello Client 1, you are connected!", b"Second message for Client 1 after 1 minute."],
    '192.168.1.2': [b"Hello Client 2, you are connected!", b"Second message for Client 2 after 1 minute."],
}

def handle_client(client_socket, addr):
    print("Connection from", addr)
    
    # Check client IP
    if addr[0] in allowed_ips or not allowed_ips:  # Allow all if the list is empty
        try:
            # Read the incoming packet
            packet = client_socket.recv(1024).decode('utf-8')
            print("Received packet:", packet)

            # Validate packet format
            if packet.startswith("+CMGR:") and packet.endswith("\r\n"):
                # Extract the string part
                string_part = packet.split("\r\n")[1]
                if string_part.startswith("^") and string_part.endswith("$"):
                    print("Valid packet received. Sending ACK...")

                    # Send ACK packet
                    ack_packet = "At+cipsend\r\n%60&"
                    try:
                        client_socket.send(ack_packet.encode('utf-8'))
                    except BrokenPipeError:
                        print("Failed to send ACK, client may have disconnected.")
                else:
                    print("Invalid string format.")
                    try:
                        client_socket.send(b"Invalid packet format.")
                    except BrokenPipeError:
                        print("Failed to send error message, client may have disconnected.")
            else:
                print("Invalid packet header.")
                try:
                    client_socket.send(b"Invalid packet format.")
                except BrokenPipeError:
                    print("Failed to send error message, client may have disconnected.")
            
            # Delay for one minute
            time.sleep(60)
            
            # Send second message
            if addr[0] in messages:
                try:
                    client_socket.send(messages[addr[0]][1])
                except BrokenPipeError:
                    print("Failed to send second message, client may have disconnected.")
            else:
                try:
                    client_socket.send(b"Unknown message for you.")
                except BrokenPipeError:
                    print("Failed to send unknown message, client may have disconnected.")
        except Exception as e:
            print(f"Error in processing data: {e}")
    else:
        print(f"Connection from {addr[0]} rejected.")
        try:
            client_socket.send(b"Access denied. You are not allowed to connect.")
        except BrokenPipeError:
            print("Failed to send access denied message, client may have disconnected.")
    
    client_socket.close()

while True:
    client, addr = tcpSocket.accept()
    
    # Create a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client, addr))
    client_thread.start()
