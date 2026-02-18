# sistema bancario e transação
import json
from pathlib import Path
from hashlib import sha256
directory = Path(__file__).resolve().parent
file_path = directory / "database.json"
def cryptography(_password):
    password = sha256(_password.encode()).hexdigest()
    return password
class Auth:
    def __init__(self):
        try:
            with open(file_path, "r", encoding="utf-8") as arq:
                self.database = json.load(arq)
        except (FileNotFoundError, json.JSONDecodeError):
            self.database = {}
    def register(self, username,password):
        if username in self.database:
            return False, "Usuário já existente!"
        self.database[username] = {"password":cryptography(password),"current balance":0, "money to receive": 0}
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Usuário cadastrado, seja bem vindo {username}! | Seu current balance é ${self.database[username]["current balance"]}"

    def user_exists(self, username):
        if username not in self.database:
            return False
        if username in self.database:
            return True
    def login(self, username, password):
        if username not in self.database:
            return False, "Usuário não encontrado!"
        else:
            if cryptography(password) != self.database[username]["password"]:
                return False, "Acesso negado!"
            return True, "Acesso concedido!"
    def transfer(self,active_user,active_password, received,amount):
        if active_user not in self.database:
            return False, "Usuário não encontrado!"
        elif received not in self.database:
            return False, "O usuário que você deseja enviar não existe!"
        if cryptography(active_password) != self.database[active_user]["password"]:
            return False, "Incorrent password!"
        if self.database[active_user]["current balance"] < amount:
            return False, "O usuário não tem saldo suficiente!"
        self.database[active_user]["current balance"] -= amount
        self.database[received]["money to receive"] += amount
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Transferência de ${amount} para {received} realizada com sucesso!\nAgora você tem ${self.database[active_user]["current balance"]}"
    def show_balance(self, user, password):
        if user not in self.database:
            return False, "Esse usuário não existe!"
        elif password != self.database[user]["password"]:
            return False, "Senha incorreta!"
        if self.database[user]["money to receive"] == "0":
            return True, f"O usuário {user} tem o saldo {self.database[user]["current balance"]}, mas ele tem {self.database[user]["money to receive"]} para receber!"
        else:
            return True, f"O usuário {user} tem o saldo ${self.database[user]["current balance"]}, mas ele tem ${self.database[user]["money to receive"]}"
    def deposit(self, user, password, amount):
        if user not in self.database:
            return False, "User not found!"
        self.database[user]["current balance"] += amount
        with open (file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Deposito feito com sucesso! Agora o usuário {user} tem o saldo de ${self.database[user]["current balance"]}"
