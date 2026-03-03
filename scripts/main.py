import os, questionary
from auth import Auth
auth = Auth()
def clean_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def bank_ui(active_user):
    options = {
        "1) Deposit ➕💵": "deposit",
        "2) Withdraw ➖💸": "withdraw",
        "3) Transfer 🔄💰": "transfer",
        "4) Refresh 🔄": "refresh",
        "5) Exit 🚪": "exit"
    }
    info = auth.show_info(active_user)
    bank_ui = f"""╔════════════════╗
║  🏦 BANKSTACK  ║
╚════════════════╝
👤 Username :  {active_user}
💰 Current balance:  ${info["current balance"]:.2f}
📥 Pending Incoming: ${info["pending incoming"]:.2f}"""
    print(bank_ui)
    select = questionary.select(
    "---------------------------",
    choices=list(options.keys())
    ).ask()
    return options[select]

def user_auth(type):
        while True:
            clean_terminal()
            username = questionary.text("Enter your username(Digit 0 to return): ").ask()
            if username == "0":
                 clean_terminal()
                 break
            password = questionary.password("Enter your password: ").ask()
            result = getattr(auth, type)(username,password)
            if type == "register" and result[0] == True:
                 print(f"{result[1]} | Press enter return")
                 input("")
                 continue
            if result[0]:
                print(f"{result[1]} | Press enter in your account")
                input("")
                return username
            print(f"{result[1]} | Press enter to try again")
            input("")
while True:
    while True:
        user_input = questionary.select(
            "Menu",
            choices=[
                "🔐 Login",
                "📝 Register"
            ]
        ).ask()
        user_input = "login" if user_input == "🔐 Login" else "register"
        if user_input == "login":
            username = user_auth("login")
            break
        if user_input == "register":
            username = user_auth("register")
            continue
    while True:
        clean_terminal()
        user_info = auth.show_info(username)
        user_input = bank_ui(username)
        if user_input == "deposit":
                while True:
                    try:
                        amount = float(questionary.text("> Deposit amount: ").ask())
                        if auth.deposit(username, amount):
                            print(f"Transfer succesful!")
                            input("")
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                        input("")
        elif user_input == "withdraw":
            print(auth.withdraw(username)[1])
            input("")
        elif user_input == "transfer":
            recipient = questionary.text("> Enter recipient username: ").ask()
            amount = float(questionary.text("> Enter amount to transfer: ").ask())
            while True:
                confirm = questionary.confirm(f"Confirm transfer of ${amount} to {recipient}").ask()
                if confirm:
                    break
                else:
                    break
            if confirm:
                result = auth.transfer(username, recipient, amount)
                print(f"* {result[1]}")
                input("")
            else:
                continue
        elif user_input == "refresh":
            continue
        elif user_input == "exit":
            questionary.press_any_key_to_continue("Press any key to exit...").ask()
            clean_terminal()
            break
