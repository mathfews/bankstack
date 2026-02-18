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
            password = input("Enter your password: ")
            result = getattr(auth, type)(username,password)
            if type == "register" and result[0] == True:
                 print(f"{result[1]} | Press enter to go to login")
                 input("")
                 user_auth("login")
            elif result[0] == True:
                print(result[1])
            print(f"{result[1]} | Press enter to try again")
            input("")
while True:
    print("Menu \n🔐1) Login\n📝2) Register")
    user_input = input("> ").strip().lower()
    if user_input == "1" or user_input == "login":
        user_auth("login")
    if user_input == "2" or user_input == "register":
        user_auth("register")