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
            return False, "User already exists!"
        self.database[username] = {"password":cryptography(password),"current balance":0, "pending incoming": 0}
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Account created! Welcome, {username}! | Your current balance is ${self.database[username]["current balance"]}"
    def withdraw(self, username):
        if username not in self.database:
            return False, "* User not found!"
        if self.database[username]["pending incoming"] == 0:
            return False, "* No pending incoming funds!"
        self.database[username]["current balance"] += self.database[username]["pending incoming"]
        self.database[username]["pending incoming"] = 0
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, "* Withdrawal successful!"
    def login(self, username, password):
        if username not in self.database:
            return False, "* User not found!"
        else:
            if cryptography(password) != self.database[username]["password"]:
                return False, "* Acess denied!"
            return True, "* Access granted!"
    def transfer(self,active_user, recipient,amount):
        if amount <= 0:
            return False, "* Please enter a positive number!"
        if active_user not in self.database:
            return False, "* User not found!"
        elif recipient not in self.database:
            return False, "* Target user does not exit!"
        if self.database[active_user]["current balance"] < amount:
            return False, "Insufficient balance!"
        self.database[active_user]["current balance"] -= amount
        self.database[recipient]["pending incoming"] += amount
        with open(file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        return True, f"Transaction of ${amount} to {recipient} processed sucessfully!\nYour current balance is {self.database[active_user]["current balance"]}"
    def show_info(self, username):
        if username in self.database:
            with open (file_path, "r", encoding="utf-8") as arq:
                self.database = json.load(arq)
            info = {
                "current balance": self.database[username]["current balance"],
                "pending incoming": self.database[username]["pending incoming"],
                "password": self.database[username]["password"]
            }
            return info
        else:
            return False, "* User not found!"
    def deposit(self, user, amount):
        if user not in self.database:
            return False, "User not found!"
        self.database[user]["current balance"] += amount
        with open (file_path, "w", encoding="utf-8") as arq:
            json.dump(self.database, arq, indent=4, ensure_ascii=False)
        balance = self.database[user]["current balance"]
        return True, f"Deposit successful! Your current balance is ${balance:.2f}"
