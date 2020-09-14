"""Клиент версия приложения для хранения паролей, которая писалась под тяжелыми наркотиками"""

from client import DataBase
from client import Network_client_tools
from client import CommandHandler

public_key = b'secret'
private_key = b'supersecret'

address = ("SECRET", 5679)


if __name__ == "__main__":
    # login = input("login: ")
    # password = input("password: ")

    login = 'secret'
    password = 'secret'

    Note = DataBase.DataBase("data.json", public_key, private_key)

    while True:
        server_socket = Network_client_tools.connect(address)

        Network_client_tools.update_client(server_socket, login, password, private_key)

        #Здесь нужно будет навести красоту
        commander = CommandHandler.CommandHandler(Note)
        commander.command_handler(input())

        server_socket = Network_client_tools.connect(address)

        Network_client_tools.update_server(server_socket, login, password, private_key)
