import socket
import threading
import time
import datetime

ip = '0.0.0.0'
port = 4404
tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSocket.bind((ip, port))
tcpSocket.listen(5)

print("Server is listening on port", port)

# نگهداری اطلاعات کلاینت‌ها
client_connections = {}
client_count = 0

# پیام‌های مختلف برای کلاینت‌های مختلف
client_messages = {
    0: ["hi tehran", "nice to me to"],
    1: ["hi shiraz", "nice to me to"],
    2: ["hi mashhad", "nice to me to"],
    3: ["hi tabriz", "nice to me to"]
}

def create_sample_packet():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%y/%m/%d,%H:%M:%S")
    packet = f'+CMGR: "REC UNREAD","SRVGPRS","","{formatted_time}+0330"\r\n^Sample string$\r\n'
    return packet.encode('utf-8')

def send_message(client_socket, message):
    try:
        client_socket.send(message.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def handle_client(client_socket, addr, client_id):
    print(f"New connection from {addr}, Client ID: {client_id}")
    
    client_connections[addr] = datetime.datetime.now()
    client_specific_messages = client_messages.get(client_id % len(client_messages))
    message_index = 0
    
    try:
        while True:
            current_time = datetime.datetime.now()
            connection_time = client_connections.get(addr)
            if connection_time and (current_time - connection_time).days > 30:
                print(f"Client {addr} connection expired (30 days limit)")
                break

            try:
                # 1. Send Sample Packet
                sample_packet = create_sample_packet()
                client_socket.send(sample_packet)
                print(f"Sent Sample Packet to {addr}")

                time.sleep(0.5)  # Short delay

                # 2. Send ACK
                ack_packet = "At+cipsend\r\n%60&"
                client_socket.send(ack_packet.encode('utf-8'))
                print(f"Sent ACK to {addr}")

                time.sleep(0.5)  # Short delay

                # 3. Send normal message
                current_message = client_specific_messages[message_index]
                if send_message(client_socket, current_message):
                    print(f"Sent message '{current_message}' to {addr}")
                else:
                    print(f"Failed to send message to {addr}. Closing connection.")
                    break
                
                message_index = (message_index + 1) % len(client_specific_messages)
            except Exception as e:
                print(f"Error in communication with {addr}: {e}")
                break

            time.sleep(60)

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        try:
            client_socket.close()
            del client_connections[addr]
        except:
            pass
        print(f"Connection closed with {addr}")
        
def accept_connections():
    global client_count
    while True:
        try:
            client, addr = tcpSocket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client, addr, client_count))
            client_thread.daemon = True
            client_thread.start()
            client_count += 1
        except Exception as e:
            print(f"Error accepting connection: {e}")
            time.sleep(1)

# شروع thread اصلی پذیرش اتصال‌ها
main_thread = threading.Thread(target=accept_connections)
main_thread.daemon = True
main_thread.start()

# نگه داشتن برنامه
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nServer shutting down...")
    tcpSocket.close()
