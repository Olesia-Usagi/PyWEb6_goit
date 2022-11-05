import socket


def main():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = 5000
    print(f'Server starting from {host}; {port}.')
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(3)
    try:
        conn, address = server_socket.accept()
        print(f'Got connection from {address}')
        message = 'Hello there!'
        while message.lower().strip() != 'break':
            print('Now wait for message from client...')
            data = conn.recv(100).decode()

            if not data:
                print('Client breaks the connection.')
                break

            print(f'Client send a message:\n|{data}|')

            message = input('---> ')
            conn.send(message.encode())
        print('Server is closed manually.')
        server_socket.close()
        conn.close()
    except KeyboardInterrupt:
        print('Connection interrupted manually.')
        server_socket.close()


if __name__ == '__main__':
    main()
