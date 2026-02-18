import os
from auth import Auth
auth = Auth()
def clean_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def bank_ui(active_user):
    info = auth.show_info(active_user)
    bank_ui = f"""╔════════════════╗
║  🏦 BANKSTACK  ║
╚════════════════╝
👤 Username :  {active_user}
💰 Current balance:  ${info["current balance"]}
📥 Pending Incoming: ${info["pending incoming"]}
---------------------------
1) Deposit ➕💵
2) Withdraw ➖💸
3) Transfer 🔄💰
4) Exit 🚪"""
    print(bank_ui)

def user_auth(type):
        while True:
            clean_terminal()
            username = input("Enter your username(Digit 0 to return): ")
            if username == "0":
                 clean_terminal()
                 break
            password = input("Enter your password: ")
            result = getattr(auth, type)(username,password)
            if type == "register" and result[0] == True:
                 print(f"{result[1]} | Press enter return")
                 input("")
                 break
            if result[0]:
                print(f"{result[1]} | Press enter in your account")
                input("")
                return username
            print(f"{result[1]} | Press enter to try again")
            input("")
while True:
    print("Menu \n🔐1) Login\n📝2) Register")
    user_input = input("> ").strip().lower()
    if user_input == "1" or user_input == "login":
        username = user_auth("login")
    if user_input == "2" or user_input == "register":
        user_auth("register")
    while True:
         clean_terminal()
         bank_ui(username)
         user_input = input("> ").strip().lower()
         if user_input == "deposit" or user_input == "1":
                while True:
                    try:
                        amount = float(input("Deposit amount: "))
                        auth.deposit(username, amount)
                    except (ValueError):
                        "Invalid input. Please enter a valid number."
                