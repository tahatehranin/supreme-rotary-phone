import socket

# تنظیمات سرور
server_ip = '127.0.0.1'  # یا آدرس IP سرور
server_port = 4401

# ایجاد سوکت
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # اتصال به سرور
    client_socket.connect((server_ip, server_port))
    print("Connected to server at {}:{}".format(server_ip, server_port))

    while True:
        # دریافت پیام از سرور
        message = client_socket.recv(1024).decode()  # حداکثر 1024 بایت

        if not message:
            break  # اگر پیامی وجود نداشت، حلقه را ترک کن

        # نمایش پیام دریافت شده
        print("Received:", message)

finally:
    # قطع ارتباط
    client_socket.close()
    print("Connection closed.")