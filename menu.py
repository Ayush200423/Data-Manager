import secure
import image_manager
from database import db_manager

from colorama import Fore

def options(username, fernet, salt):
    option_selected = input(Fore.WHITE + "(A)dd | (V)iew | (D)elete | (Q)uit? ").lower()
    if option_selected == "a":
        append(username, fernet, salt)
    elif option_selected == "v":
        read(username, fernet, salt)
    elif option_selected == "d":
        delete(username, fernet, salt)
        pass
    elif option_selected == "q":
        terminate()    
    else:
        print(Fore.RED + "Input not valid.")
    options(username, fernet, salt)

def append(username, fernet, salt):
    print("Press Enter to Go Back.")
    entry_type = input("(W)ebsite or (I)mage: ").lower()
    if entry_type == "w":
        website = input("Website: ").lower()
        check_entry(website, username, fernet, salt)
        website_user = input("Username: ")
        check_entry(website_user, username, fernet, salt)
        website_pass = input("Password: ")
        check_entry(website_pass, username, fernet, salt)
        encrypted_pass = secure.encrypt_value(website_pass, fernet, 'password')
        db_manager.insert_record(username, salt, website, website_user, encrypted_pass)
        print(f"{Fore.GREEN + website.capitalize()} added successfully.")
    elif entry_type == "i":
        image_title, image_description, bytesform = image_manager.attach_image()
        encrypted_img_form = secure.encrypt_value(bytesform, fernet, 'image')
        db_manager.insert_record(username, image_title, image_description, encrypted_img_form)
        print(Fore.GREEN + f"{image_title} added successfully.")
    return options(username, fernet, salt)

def read(username, fernet, salt):
    view_type = input("(W)ebsite or (I)mage: ").lower()
    if view_type == "w":
        website_input = input("Which credentials would you like to view? Press (1) to view all: ").lower()
        credentials_list = db_manager.read_record(username, "credentials")
        if website_input == "1":
            for credential in credentials_list:
                if credential[2] != None:
                    print(f"Website: {credential[2].capitalize()}, Username: {credential[3]}, Password: {secure.decrypt_value(credential[4], fernet, 'password')}")
        else:
            for credential in credentials_list:
                if credential[2] == website_input:
                    print(f"Website: {credential[2]}, Username: {credential[3].capitalize()}, Password: {secure.decrypt_value(credential[4], fernet, 'password')}")
    elif view_type == "i":
        image_input = input("Which image would you like to view? Press (1) to view all image titles: ").lower()
        images_list = db_manager.read_record(username, "images")
        if image_input == "1":
            for image in images_list:
                print(image[1])
        else:
            for image in images_list:
                if image[1] == image_input:
                    print(f"Image title: {image[1]}")
                    print(f"Image description: {image[2]}")
                    byteform = secure.decrypt_value(image[3], fernet, 'image')
                    image_manager.read_image(byteform)
    return options(username, fernet, salt)

def delete(username, fernet, salt):
    delete_item = input("(A)ccount / (C)redential / (I)mage: ").lower()
    if delete_item == "a":
        confirm = input("Type 'YES' to Confirm (This cannot be undone!): ").lower()
        if confirm == "yes":
            db_manager.delete_record(username, account = True)
            terminate()
    elif delete_item == "c":
        delete_website = input("Which website would you like to delete: ")
        check_entry(delete_website, username, fernet, salt)
        confirm = input("Type 'YES' to Confirm (This cannot be undone!): ").lower()
        if confirm == "yes":
            try:
                db_manager.delete_record(username, website = delete_website)
                print(Fore.RED + f"{delete_website.upper()} has been deleted.")
            except:
                print(Fore.RED + Exception)
    elif delete_item == "i":
        delete_image = input("Which image would you like to delete: ")
        check_entry(delete_image, username, fernet, salt)
        confirm = input("Type 'YES' to Confirm (This cannot be undone!): ").lower()
        if confirm == "yes":
            try:
                db_manager.delete_record(username, title = delete_image)
                print(Fore.RED + f"{delete_image.upper()} has been deleted.")
            except:
                print(Fore.RED + Exception)
    return options(username, fernet, salt)

def check_entry(entry, username, fernet, salt):
    if entry == "":
        print(Fore.RED + "Entry not recorded.")
        return options(username, fernet, salt)
    return

def terminate():
    db_manager.close_conn()
    quit()