"""Класс описывающий логику работы базы данных (JSON-пакет не лучший выбор)"""

import os
import rsa
import json
import pyaes


class DataBase():
    def __init__(self, name, public_key, private_key):
        self.name = name
        self.public_key = rsa.PublicKey.load_pkcs1(public_key)
        self.private_key = rsa.PrivateKey.load_pkcs1(private_key)

    def search_data(self, word):
        result = {}
        data = self.__load_data()
        for key in data:
            if word in key:
                result[key] = data[key]
        self.__write_data(data)
        return result

    def add_data(self, data):
        try:
            old_data = self.__load_data()
            if type(data) == dict and type(old_data) == dict:
                for key in old_data:
                    if key not in data:
                        data[key] = old_data[key]
                return self.__write_data(data)
            else:
                return "Error"
        except json.decoder.JSONDecodeError:
            if type(data) == dict:
                return self.__write_data(data)
            else:
                return "Error"

    def delete_data(self, keys):
        data = self.__load_data()
        log_out = ""
        for key in keys:
            try:
                del data[key]
                log_out += "Deleted successfully: %s \n" % key
            except KeyError:
                log_out += "Deleted failed (key error): %s \n" % key
        self.__write_data(data)
        return log_out

    def delete_all(self):
        print("Are you sure you want to delete all data? Removal is irreversible. (type y/n)")
        while True:
            agreement = input()
            if agreement.lower() == "y":
                self.__write_data({})
                return "Deleted successfully..\n"
            elif agreement.lower() == "n":
                return ""


    def return_data(self, keys=None):
        data = self.__load_data()
        if not keys:
            out = data
        else:
            out = {}
            for key in keys:
                try:
                    out[key] = data[key]
                except KeyError:
                    pass
        self.__write_data(data)
        return out

    def print_data(self):
        data = self.__load_data()
        self.__write_data(data)
        print(data)

    def __encode(self, data):
        session_key = os.urandom(32)

        aes = pyaes.AESModeOfOperationCTR(session_key)
        crypt = aes.encrypt(data)

        crypt_key = rsa.encrypt(session_key, self.public_key)
        with open("session_encrypted_key", "wb") as key_file:
            key_file.write(crypt_key)

        return crypt

    def __decode(self, data):
        with open("session_encrypted_key", "rb") as key_file:
            crypt_key = key_file.read()
        decrypt_key = rsa.decrypt(crypt_key, self.private_key)
        aes = pyaes.AESModeOfOperationCTR(decrypt_key)
        decrypt_data = aes.decrypt(data)
        return decrypt_data

    def __load_data(self):
        try:
            with open(self.name, "r") as json_read:
                data = json.load(json_read)
                return data
        except:
            with open(self.name, "rb") as byte_read:
                crypt_data = byte_read.read()
            with open(self.name, "wb") as byte_write:
                byte_write.write(self.__decode(crypt_data))
            with open(self.name, "r") as json_read:
                data = json.load(json_read)
                return data

    def __write_data(self, data):
        with open(self.name, "w") as json_write:
            json.dump(data, json_write)
        with open(self.name, "rb") as byte_read:
            data = byte_read.read()
        with open(self.name, "wb") as byte_write:
            byte_write.write(self.__encode(data))
        return "Data saved successfully!"
