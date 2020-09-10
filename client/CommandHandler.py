"""Упоротый комманд хэндлер, который нужно переписать, кажется"""


class CommandHandler():
    options_name = {'export': ['--export', '>>', '>', '-e'], 'all': ['--all', '-a'], 'search': ['--search', '-s'],
                    "import": ["--import", "-i", "<<", "<"], "noprint": ["--noprint", "-np", "-"]}

    command_name = {'mydump': ['mydump', 'md'], 'mypasswords': ['mypasswords', 'mp'],
                    'addpasswords': ['addpasswords', 'ap'], 'delpasswords': ['delpasswords', 'dp', 'del', 'rm']}

    def __init__(self, data_base):
        self.data_base = data_base

    def comm_mypasswords(self, options):
        list_act = "print"
        file = None

        this_command = self.belong(self.options_name['export'], options)
        if this_command:
            list_act += "export"
            file = options[options.index(this_command) + 1]

            del options[options.index(this_command) + 1], options[options.index(this_command)]

        this_command = self.belong(self.options_name['all'], options)
        if this_command or not options:
            self.out_act(list_act, self.dict_to_str(self.data_base.return_data()), file)
            return

        this_command = self.belong(self.options_name['search'], options)
        if this_command:
            phrase = self.arr_to_str(options[options.index(this_command) + 1:])
            self.out_act(list_act, self.dict_to_str(self.data_base.search_data(phrase)), file)
            return

        self.out_act(list_act, self.dict_to_str(self.data_base.return_data(options)), file)

    def comm_addpasswords(self, options):
        this_command = self.belong(self.options_name['import'], options)
        if this_command:
            # когда-нибудь я сделаю это
            print("ИМПОРТ ПАРОЛЕЙ ИЗ ФАЙЛА ", options[options.index(this_command) + 1])
            del options[options.index(this_command) + 1], options[options.index(this_command)]
            return
        else:
            print(self.data_base.add_data(self.parse_in_password(options)))

    def comm_delpasswords(self, options):
        this_command = self.belong(self.options_name['all'], options)
        if this_command:
            print(self.data_base.delete_all(), end="")
        else:
            print(self.data_base.delete_data(options))

    def command_handler(self, inp):
        inp_parse = inp.split(" ")

        if inp_parse[0] in self.command_name["mydump"]:
            inp_parse = inp_parse[1:]

        if inp_parse[0] in self.command_name["mypasswords"]:
            self.comm_mypasswords(inp_parse[1:])

        elif inp_parse[0] in self.command_name['addpasswords']:
            self.comm_addpasswords(inp_parse[1:])

        elif inp_parse[0] in self.command_name['delpasswords']:
            self.comm_delpasswords(inp_parse[1:])

        else:
            print("command not found")

    @staticmethod
    def belong(set_one, set_two):
        for elem in set_one:
            if elem in set_two:
                return elem

    @staticmethod
    def out_act(act, data, file=None):
        if "print" in act:
            print(data)
        if "export" in act:
            with open(file, "w") as wr_file:
                wr_file.write(data)

    @staticmethod
    def parse_in_password(args):
        password_base = {}

        for arg in args:
            arg.replace(": ", ":")
            arg.replace(" :", ":")

            try:
                base_name, base_password = arg.split(":")
                password_base[base_name] = base_password
            except ValueError:
                try:
                    if arg != "" and password_base[base_name] == "":
                        password_base[base_name] = arg
                except UnboundLocalError:
                    print("incorrect input")

        return password_base

    @staticmethod
    def dict_to_str(dict_file):
        str_file = ""
        for key in dict_file:
            str_file += key + "  " + dict_file[key] + "\n"
        return str_file

    @staticmethod
    def arr_to_str(arr_file):
        str_file = ""
        for word in arr_file:
            str_file += word + " "
        return str_file[:-1]
