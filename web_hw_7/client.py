import socket


def client():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    try:
        message = input('Write a message or send "stop" to cut the connection:  ')

        while message.lower().strip() != 'stop':
            print('Waiting for server reply/')
            try:
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
                if data == 'stop':
                    print('Connection with server lost.')
                    break
            except ConnectionAbortedError:
                print('Connection with server lost.')
                break

            print(f'Message from {host}/server: {data} ')
            message = input('--> ')
        print('Connection dismissed.')
        client_socket.close()
    except KeyboardInterrupt:
        print('Connection interrupted manually!')
        client_socket.close()


if __name__ == '__main__':
    client()
