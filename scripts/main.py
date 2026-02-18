import os
from auth import Auth
auth = Auth()
def clean_terminal():
    os.system("cls" if os.name == "nt" else "clear")
def user_auth(type):
        while True:
            clean_terminal()
            username = input("Enter your username(Digit 0 to return): ")
            if username == "0":
                clean_terminal()
                break
            while True:
                if type == "login" and auth.user_exists(username) == False:
                    clean_terminal()
                    print(f"O usuário {username} não foi encontrado!")
                    username = input("Enter your username(Digit 0 to return): ")
                elif type == "login" and auth.user_exists(username) == True:
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
                break
            print(f"{result[1]} | Press enter to try again")
            input("")
while True:
    print("Menu \n🔐1) Login\n📝2) Register")
    user_input = input("> ").strip().lower()
    if user_input == "1" or user_input == "login":
        user_auth("login")
    if user_input == "2" or user_input == "register":
        user_auth("register")
    clean_terminal()