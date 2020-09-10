"""Клиент версия приложения для хранения паролей, которая писалась под тяжелыми наркотиками"""

from release.client_assembly_one import DataBase
from release.client_assembly_one import Network_client_tools
from release.client_assembly_one import handler

public_key = b'secret'
private_key = b'supersecret'

address = ("192.168.56.1", 5679)


if __name__ == "__main__":
    # login = input("login: ")
    # password = input("password: ")

    login = 'secret'
    password = 'secret'

    Note = DataBase.DataBase("data.json", public_key, private_key)

    while True:
        server_socket = Network_client_tools.connect(address)

        Network_client_tools.update_client(server_socket, login, password, private_key)

        #command_handler(input()) Здесь надо будет навести красоту
        commander = handler.CommandHandler(Note)
        commander.command_handler(input())

        server_socket = Network_client_tools.connect(address)

        Network_client_tools.update_server(server_socket, login, password, private_key)
