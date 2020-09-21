import socket
SEP = b"//sep//"


def connect(addr):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(addr)
    return server_socket


def verifications(server_sock, private_key):
    crypt_message = server_sock.recv(1024)
    encrypt_message = aese.rsa_decrypt(crypt_message, private_key)
    server_sock.send(encrypt_message)
    return server_sock.recv(1024).decode("utf8")


def authorization_(server_sock, login, password, command):
    connect_response = command.encode("utf8") + SEP + login.encode("utf8") + SEP + password.encode('utf8')
    server_sock.send(connect_response)
    return server_sock.recv(1024).decode("utf8")


def update_server(server_sock, login, password, private_key):
    command = "update_server"
    aut = authorization_(server_sock, login, password, command)

    if aut == "Авторизация прошла успешно":
        ver = verifications(server_sock, private_key)
    else:
        ver = None 

    if ver == "Проверка ключа прошла успешно":
        with open("data.json", "rb") as read_file:
            data = read_file.read()
        data += b"//end//"
        with open("session_encrypted_key", "rb") as read_key:
            data += read_key.read()
        data += b"//end//"
        server_sock.sendall(data)

    res = server_sock.recv(1024).decode("utf8")
    return aut, ver, res


def update_client(server_sock, login, password, private_key):
    command = "update_client"
    aut = authorization_(server_sock, login, password, command)

    if aut == "Авторизация прошла успешно":
        ver = verifications(server_sock, private_key)
    else:
        ver = None

    if ver == "Проверка ключа прошла успешно":
        data = b""
        count_file = 0
        while True:
            data_peaks = server_sock.recv(1024)
            data += data_peaks
            if b"//end//" in data_peaks:
                count_file += data_peaks.count(b"//end//")
            if count_file > 1:
                break

        data = data.split(b"//end//")
        with open("data.json", "wb") as write_file:
            write_file.write(data[0])
        with open("session_encrypted_key", "wb") as write_key:
            write_key.write(data[1])

    return aut, ver
