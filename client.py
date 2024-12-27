import socket
import time

def main():
    host = '127.0.0.1'
    port = 4404

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                break
            print("Received:", data.decode('utf-8'))

            # Simulate processing time
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
