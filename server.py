import socket
import threading
import time

ip = '0.0.0.0'  # Listen on all interfaces
port = 4401
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.bind((ip, port))
tcpSocket.listen(5)

print("Server is listening on port", port)

# لیست IP های مجاز
allowed_ips = ['127.0.0.1', '192.168.1.2']

# پیام‌های متفاوت برای هر کلاینت بر اساس IP
messages = {
    '127.0.0.1': [b"Hello Client 1, you are connected!", b"Second message for Client 1 after 1 minute."],
    '192.168.1.2': [b"Hello Client 2, you are connected!", b"Second message for Client 2 after 1 minute."],
}

def handle_client(client_socket, addr):
    print("Got connection from", addr)
    
    # بررسی IP کلاینت
    if addr[0] in allowed_ips:
        # Read the incoming packet
        packet = client_socket.recv(1024).decode('utf-8')
        print("Received packet:", packet)

        # Validate the packet format
        if packet.startswith("+CMGR:") and packet.endswith("\r\n"):
            # Extract the string part
            string_part = packet.split("\r\n")[1]
            if string_part.startswith("^") and string_part.endswith("$"):
                print("Valid packet received. Sending ACK...")

                # Send ACK packet
                ack_packet = "At+cipsend\r\n%60&"
                client_socket.send(ack_packet.encode('utf-8'))
            else:
                print("Invalid string format.")
                client_socket.send(b"Invalid packet format.")
        else:
            print("Invalid packet header.")
            client_socket.send(b"Invalid packet format.")
        
        # تأخیر یک دقیقه‌ای
        time.sleep(60)
        
        # ارسال پیام دوم
        client_socket.send(messages[addr[0]][1])
    else:
        print(f"Connection from {addr[0]} rejected.")
        client_socket.send(b"Access denied. You are not allowed to connect.")
    
    client_socket.close()

while True:
    client, addr = tcpSocket.accept()
    
    # ایجاد یک ترد برای مدیریت کلاینت
    client_thread = threading.Thread(target=handle_client, args=(client, addr))
    client_thread.start()
