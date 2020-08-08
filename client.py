import aese
import socket
from demo import DataBase

name = "data.json"
SEP = b"//sep//"
address = ("SECRET", 5679)
public_key = b'-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAljZIP9zkFqH5a8Z0GKTdm9VYOkr+vCmx7Atjs3aEtK6PisCe/QLv\n45SNyUcVVbAVe3mH4+CR9aJoK5UnIibONbQFmBQr19+wbir8jq28AS92daMD5M9x\nVEvkMXhin6iJJnr1sEX65WXzQMSe2EsWFssyCjhk8sv37n8U52clGzSNFhwUwnRM\nUcE3YiDwpf//SOIVc+cBxOH5BYZtLbjAG+Yy2D8akoH2J/aUZkIHguPMcPBlr+gr\n0+h+iA3XZZVJsu2n2c0MjiWbg/7INBvx67FqEAqOHOmJA4gvj7edht5jhb+cYJ/X\nlzWOnSCjCbDETKhlYLJuJxfnQvkH+WXUjQIDAQAB\n-----END RSA PUBLIC KEY-----\n'
private_key = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEqQIBAAKCAQEAljZIP9zkFqH5a8Z0GKTdm9VYOkr+vCmx7Atjs3aEtK6PisCe\n/QLv45SNyUcVVbAVe3mH4+CR9aJoK5UnIibONbQFmBQr19+wbir8jq28AS92daMD\n5M9xVEvkMXhin6iJJnr1sEX65WXzQMSe2EsWFssyCjhk8sv37n8U52clGzSNFhwU\nwnRMUcE3YiDwpf//SOIVc+cBxOH5BYZtLbjAG+Yy2D8akoH2J/aUZkIHguPMcPBl\nr+gr0+h+iA3XZZVJsu2n2c0MjiWbg/7INBvx67FqEAqOHOmJA4gvj7edht5jhb+c\nYJ/XlzWOnSCjCbDETKhlYLJuJxfnQvkH+WXUjQIDAQABAoIBADou0nNyMyMVIFB/\nsS5uhaw7yg3iSKNHnzQoATldWe/GgbEkBTFJdvP28aiaEQh8yQVnwJwiu0ai3qir\nAFp5H3yru1L51TWr3mH94o+9ecoXwVG1j+eL9oDJWJ1U3RasqFswW4QoxxMeF0fq\nIQD0rJytnjdZOrjVCnpJ2IHAbVemJLtr+OCd4i/irH2cmaN4Rhitj/3Lukzb/CJ/\nRp7lNrnLWjowF66/pPVuiVJENWuh1i7Sl2HWzvSUouiIJ9WYms0PgOwZMspXbvBP\npjPTPKpbRQZYffUgdu+vWIaRo+v6M6+ltp9BwVuCn2wrD9hjkhlwqdBiVEr/BeDl\nBPEoHd0CgYkAnHltG9V7DBqEx+0QL26SbT6/BxQKaAm6vTvmiZa2nMZYXIrz9QA0\nziSNsScXobVBd/XJTZP42kJq3gCgDp/VCpq2wT+BPGHQFzYc178eduIe6zivxHuR\n1qNcP2vG+UKUZrRBj/QmRnowLVN4n0z6PrvhNsLJ2ZOLi1UNLErU20V4UUwlHSuG\n1wJ5APXBLKPDj2Bp3pQ8X+8tT2Uf+XlmYbJYjCEloFQrAjuXCalAJsXhZnO4MeI/\nEMmBgE4Jo1ZlRTOsN3ZBPhPKVc6AXGag6E47A9dKS/X/Uy/qRje3Mx+LUu0DUEKH\nCg+QMev1Meav/1xL6n5iKvvwF4UDsbL1dGUnOwKBiQCGVPxlo92SI4YQuSVnAw80\nOGT5J6xTat7lLHKbdkbpyqH7ONN9ZyLuQpVeG8h+7EP7P4gFUN6YSeLDGlhOlcro\n4q+4sdM6SmLCOpOCaLI3r6KJn83N6aPnV7GPRPC59v2+Okv60Mi3QpjvoLRyVjyT\n9OnBAHMXlkJ7aJX5i3i3kilb6foG0+JbAngrY77w7w86c5bDz2EUxog1D48pewUW\nywF6vLzw/2L2iHVBN71gxKolFklga8gX+9Bedt8q2th8BhUIwP4n2lqKCinGSPSb\nE1pbQZflx/21AQUCw0q4cA3lIOejx1nkY44c3f7AfyRz9Edjpwt1ze8pIfzW3vV9\nAo8CgYg1WjH2Ix9fjm2u6uJwWdQnmucrRpMhJ08p6d1NqQPUmkI//kwLfgkib0Eg\nZFtGEKL79gwI1lpl1c0dD6552ED6/rUd7Um7xvoM+oUD2sFhfZSPc0qQaCY45RdW\nuEBa/oynVZbUNlyYnwofrz5p4kU91Vn4ThklH47cJDy39Hgz9QSOTkOSLn0Z\n-----END RSA PRIVATE KEY-----\n'


def verifications(server_sock, private_key):
    crypt_message = server_sock.recv(1024)
    encrypt_message = aese.rsa_decrypt(crypt_message, private_key)
    server_sock.send(encrypt_message)
    return server_sock.recv(1024).decode("utf8")

# авторизация и отправка команды
def authorization_(server_sock, login, password, command):
    connect_response = command.encode("utf8") + SEP + login.encode("utf8") + SEP + password.encode('utf8')
    server_sock.send(connect_response)
    return server_sock.recv(1024).decode("utf8")


def update_server_full(server_sock, login, password, private_key):
    command = "update_server"
    print(authorization_(server_sock, login, password, command))
    print(verifications(server_sock, private_key))
    with open("data.json", "rb") as read_file:
        data = read_file.read()
    data += b"//end//"
    server_sock.sendall(data)


def update_client_full(server_sock, login, password, private_key):
    command = "update_client"
    print(authorization_(server_sock, login, password, command))
    print(verifications(server_sock, private_key))

    data = b""
    while True:
        data_peaks = server_sock.recv(1024)
        print(data_peaks)
        data += data_peaks
        if b"//end//" in data_peaks:
            break

    data = data.split(b"//end//")
    with open("data.json", "wb") as write_file:
        write_file.write(data[0])


options_name = {'export': ['--export', '>>', '>', '-e'], 'all': ['--all', '-a'], 'search': ['--search', '-s'], "import": ["--import", "-i", "<<", "<"]}
command_name = {'mydump': ['mydump', 'md'], 'mypasswords': ['mypasswords', 'mp'], 'addpasswords': ['addpasswords', 'ap'], 'delpasswords': ['delpasswords', 'dp']}


def belong(set_one, set_two):
    for elem in set_one:
        if elem in set_two:
            return elem


# command handler
def comm_mypasswords(options):
    this_command = belong(options_name['export'], options)
    if this_command:
        print("ВЫВЕСТИ ВСЕ В ФАЙЛ", options[options.index(this_command) + 1])
        del options[options.index(this_command) + 1], options[options.index(this_command)]

    this_command = belong(options_name['all'], options)
    if this_command or options == []:
        print("НАПЕЧАТАТЬ ВСЕ")
        DATABASE.print_data()
        return

    this_command = belong(options_name['search'], options)
    if this_command:
        print("ПОИСК ПО ФРАЗЕ ", options[options.index(this_command)+1:])
        return

    print("ВЕРНУТЬ ФАЙЛЫ-ПАРОЛИ С ИМЕНЕМ", options)


def comm_addpasswords(options):
    this_command = belong(options_name['import'], options)
    if this_command:
        print("ИМПОРТ ПАРОЛЕЙ ИЗ ФАЙЛА ", options[options.index(this_command) + 1])
        del options[options.index(this_command) + 1], options[options.index(this_command)]
        return
    else:
        print('ДОБАВИТЬ ПАРОЛИ ', options)


def comm_delpasswords(options):
    this_command = belong(options_name['all'], options)
    if this_command:
        print("УДАЛИТЬ ВСЕ ПАРОЛИ")
    else:
        print('УДАЛИТЬ ПАРОЛИ ', options)




def command_handler(inp):
    inp_parse = inp.split(" ")

    if inp_parse[0] in command_name["mydump"]:
        inp_parse = inp_parse[1:]

    print(inp_parse)

    if inp_parse[0] in command_name["mypasswords"]:
        comm_mypasswords(inp_parse[1:])

    elif inp_parse[0] in command_name['addpasswords']:
        comm_addpasswords(inp_parse[1:])

    elif inp_parse[0] in command_name['delpasswords']:
        comm_delpasswords(inp_parse[1:])

    else:
        print("command not found")
# if __name__ == "__main__":
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.connect(address)

DATABASE = DataBase("data.json", public_key, private_key)
command_handler(input())
