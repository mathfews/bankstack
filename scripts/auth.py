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
        self.database[username] = {"password":cryptography(password),"current balance":0, "pending incoming": 0}
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Usuário cadastrado, seja bem vindo {username}! | Seu current balance é ${self.database[username]["current balance"]}"
    def withdraw(self, username):
        if username not in self.database:
            return False, "* Usuário não encontrado"
        if self.database[username]["pending incoming"] == 0:
            return False, "* No pending incoming funds!"
        self.database[username]["current balance"] += self.database[username]["pending incoming"]
        self.database[username]["pending incoming"] = 0
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, "* Withdrawal successful!"
    def login(self, username, password):
        if username not in self.database:
            return False, "Usuário não encontrado!"
        else:
            if cryptography(password) != self.database[username]["password"]:
                return False, "Acesso negado!"
            return True, "Acesso concedido!"
    def transfer(self,active_user,active_password, recipient,amount):
        if active_user not in self.database:
            return False, "Usuário não encontrado!"
        elif recipient not in self.database:
            return False, "O usuário que você deseja enviar não existe!"
        if active_password != self.database[active_user]["password"]:
            return False, "Incorret password!"
        if self.database[active_user]["current balance"] < amount:
            return False, "O usuário não tem saldo suficiente!"
        self.database[active_user]["current balance"] -= amount
        self.database[recipient]["pending incoming"] += amount
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Transferência de ${amount} para {recipient} realizada com sucesso!\nAgora você tem ${self.database[active_user]["current balance"]}"
    def show_balance(self, user, password):
        if user not in self.database:
            return False, "Esse usuário não existe!"
        elif password != self.database[user]["password"]:
            return False, "Senha incorreta!"
        if self.database[user]["pending incoming"] == "0":
            return True, f"O usuário {user} tem o saldo {self.database[user]["current balance"]}, mas ele tem {self.database[user]["pending incoming"]} para receber!"
        else:
            return True, f"O usuário {user} tem o saldo ${self.database[user]["current balance"]}, mas ele tem ${self.database[user]["pending incoming"]}"
    def show_info(self, username):
        if username in self.database:
            with open (file_path, "r", encoding="utf-8") as arq:
                self.database = json.load(arq)
            info = {
                "current balance": self.database[username]["current balance"],
                "pending incoming": self.database[username]["pending incoming"],
                "db_password": self.database[username]["password"]
            }
            return info
        else:
            return False, f"O usuário {username}, não existe!"
    def deposit(self, user, amount):
        if user not in self.database:
            return False, "User not found!"
        self.database[user]["current balance"] += amount
        with open (file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        balance = self.database[user]["current balance"]
        return True, f"Deposito feito com sucesso! Agora você tem o saldo de ${round(balance,2)}"
