import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("192.168.0.50", 8081))


    sock.sendall(bytes("aaaaa\n", "utf-8"))

    # Receive data from the server and shut down
    print(str(sock.recv(1024), "utf-8"))
