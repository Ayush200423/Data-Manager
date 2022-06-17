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
    master_pass_requirements = {"characters": [8,0], "number": [1,0], "letter": [1,0], "special character": [1,0]}
    requirements_tracker = 1
    all_specialChar = "!@#$%^&*()-+?_=,;:}{?\][<>/"
    if len(password) >= 8:
        master_pass_requirements["characters"][1] = 1
    for letter in password:
        if letter.isnumeric() == True:
            master_pass_requirements["number"][1] = 1
        if letter.isalpha() == True:
            master_pass_requirements["letter"][1] = 1
        if letter in all_specialChar:
            master_pass_requirements["special character"][1] = 1
    for i in master_pass_requirements.values():
        requirements_tracker *= i[1]
    if requirements_tracker == 0:
        base_error = Fore.RED + "Your password must contain "
        for key in master_pass_requirements:
            if master_pass_requirements[key][1] == 0:
                base_error += str(master_pass_requirements[key][0]) + " " + key + ", "
        print(base_error.rstrip(", ") + ".")
        db_manager.close_conn()
        quit()
    return

if __name__ == '__main__':
    db_manager.create()
    master_pass()