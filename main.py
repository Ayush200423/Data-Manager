import secure
import menu
from database import db_manager

from colorama import Fore

def master_pass():
    username = input("Username: ").upper()
    password = input("Password: ").upper()
    if db_manager.read_record(username, "verification") == []:
        create_account = input("Create Account? (Y)es - (N)o: ").lower()
        if create_account == "y":
            check_masterpass(password)
            pass_key, salt_verification = secure.hash_file(username, password, False)
            db_manager.insert_record(username, salt_verification, pass_key)
            fernet, salt_encrypt = secure.hash_to_encrypt(username, password, False)
            db_manager.insert_record(username, salt_encrypt, None, None, None)
            return menu.options(username, fernet, salt_encrypt)
        else:
            db_manager.close_conn()
            quit()
    else:
        stored_pass_key = db_manager.read_record(username, "verification")[0][2]
        pass_key = secure.hash_file(username, password, True)[0]
        if pass_key == stored_pass_key:
            print(Fore.GREEN + "Verified.")
            fernet, salt_encrypt = secure.hash_to_encrypt(username, password, True)
            return menu.options(username, fernet, salt_encrypt)
        else:
            print(Fore.RED + "Error - Wrong Password.")
            db_manager.close_conn()
            quit()

def check_masterpass(password):
    master_pass_requirements = {"characters": 0, "number": 0, "letter": 0, "specialChar": 0}
    requirements_tracker = 1
    all_specialChar = "!@#$%^&*()-+?_=,;:}{?\][<>/"
    if len(password) >= 8:
        master_pass_requirements["characters"] = 1
    for letter in password:
        if letter.isnumeric() == True:
            master_pass_requirements["number"] = 1
        if letter.isalpha() == True:
            master_pass_requirements["letter"] = 1
        if letter in all_specialChar:
            master_pass_requirements["specialChar"] = 1
    for i in master_pass_requirements.values():
        requirements_tracker *= i
    if requirements_tracker == 0:
        print(Fore.RED + "Your password must contain atleast 8 characters, 1 number, 1 letter, and 1 special character.")
        db_manager.close_conn()
        quit()

if __name__ == '__main__':
    db_manager.create()
    master_pass()