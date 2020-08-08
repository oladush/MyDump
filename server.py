import os
import aese
import socket
import hashlib

"""Временная база данных """
# base = {login:[salt, hash, public key]}
client_info = {"potato": [b"\xf7u\xe5s\xfd0\x92\x8c\xa0\xcc\x81\xf4\xd6)/\xcbI\x9a\xc4\xe2y\xe1G\x1bJ\xe9lF\xbf\xd8\x80$\x81\xa0\x90N\x8a\xf1\x89>>\xe1\xd2\\\xbe\xc4?\xb2\x8a\xaaU+\xcd\xfa?z.\xacL\xfb\x99\xc3\xbb\xb4\xf3\xe0\xb1\xe3\xd4V\x0f\x19\xdb\xc5T9i \x03\x92l\x11\x82\x15\xe6\xeb\xd2\xf4\xb9\xa5Bo\x9d)2\x07\x0c3!\xa7\x94q\x9da$\xdcAN\xc8\xd8b]\xa3\xe9\xbc\xa1\xc9\x0e\xdd\xf7\xc6\xdf\xf1LW\x109q", b'|\x96z~\x96M\xd5\xbe*$\x936\xd8%\xc1\xf2o\xbeuR\x88\x06\xe1\x06=>O:8\xe4\x7fs\x8a\xa8\xf0\x11\xech\xab\xcd,\xd4\xa0\xdb\xa3L\xd8\xc8\xef\xc8\xeb\xa2<\xfb\x8e\x87jK-.\x07z\x8eH', b'-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAljZIP9zkFqH5a8Z0GKTdm9VYOkr+vCmx7Atjs3aEtK6PisCe/QLv\n45SNyUcVVbAVe3mH4+CR9aJoK5UnIibONbQFmBQr19+wbir8jq28AS92daMD5M9x\nVEvkMXhin6iJJnr1sEX65WXzQMSe2EsWFssyCjhk8sv37n8U52clGzSNFhwUwnRM\nUcE3YiDwpf//SOIVc+cBxOH5BYZtLbjAG+Yy2D8akoH2J/aUZkIHguPMcPBlr+gr\n0+h+iA3XZZVJsu2n2c0MjiWbg/7INBvx67FqEAqOHOmJA4gvj7edht5jhb+cYJ/X\nlzWOnSCjCbDETKhlYLJuJxfnQvkH+WXUjQIDAQAB\n-----END RSA PUBLIC KEY-----\n']}


def verification(login, client_socket):
    try:
        random_message = os.urandom(128)
        public_key = client_info[login][2]
        verification_message = aese.rsa_crypt(random_message, public_key)
        client_socket.send(verification_message)
        if client_socket.recv(1024) == random_message:
            print("Проверка ключа прошла успешно")
            client_socket.send("Проверка ключа прошла успешно".encode("utf8"))
            return True
        else:
            print("В доступе отказано. Убедитесь в правильности вашего приватного ключа.")
            client_socket.send("В доступе отказано. Убедитесь в правильности вашего приватного ключа.".encode("utf8"))
            return False
    except KeyError:
        print("Такого пользователя не сущевствует")
        client_socket.send("Такого пользователя не сущевствует".encode("utf8"))
        return False


# поколдовать с исключениями
def authorization(login, password, client_socket):
    try:
        hash_password = hashlib.pbkdf2_hmac("sha512", password, client_info[login][0], 1024, None)
        if hash_password == client_info[login][1]:
            print("Авторизация прошла успешно")
            client_socket.send("Авторизация прошла успешно".encode("utf8"))
            return True
        else:
            print("Неверный пароль")
            client_socket.send("Неверный пароль".encode("utf8"))
            return False
    except:
        print("Что-то пошло не так. Повторите попытку позже.")
        client_socket.send("Что-то пошло не так. Повторите попытку позже.".encode("utf8"))


def update_client(login, client_socket):
    file_name = login + ".json"
    with open(file_name, "rb") as read_data:
        data = read_data.read()
        print(data)
        data += b"//end//"
    client_socket.sendall(data)


def update_server(login, client_socket):
    data = b""
    while True:
        data_peaks = client_socket.recv(1024)
        print(data_peaks)
        data += data_peaks
        if b"//end//" in data_peaks:
            break
    data = data.split(b"//end//")
    file_name = login + ".json"
    with open(file_name, "wb") as write_data:
        write_data.write(data[0])
    client_socket.send("Данные успешно обновлены".encode("utf8"))


if __name__ == "__main__":
    # start server
    address = ("192.168.56.1", 5679)
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host.bind(address)
    host.listen(100)

    while True:
        client, addr = host.accept()
        command, login, password = client.recv(128).split(b"//sep//")
        login = login.decode("utf8")
        if authorization(login, password, client) and verification(login, client):
            if command == b"update_server":
                update_server(login, client)
            elif command == b"update_client":
                update_client(login, client)
        else:
            client.send("Миграция не удалась".encode('utf8'))
