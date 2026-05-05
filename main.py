import json

def save_passwords(passwords):
    with open("passwords.json", "w") as f:
        json.dump(passwords, f)

def load_passwords():
    try:
        with open("passwords.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    passwords=load_passwords()
    while True:
        print("\nPick the index of the action:")
        print("1. Add password")
        print("2. View passwords")
        print("3. Edit password")
        print("4. Exit")
        choice=input("Enter your choice: ")
        if choice=="1":
            add(passwords)
            print("Password added successfully.")
        elif choice=="2":
            view(passwords)
        elif choice=="3":
            edit(passwords)
        elif choice=="4":
            print("Exiting...")
            save_passwords(passwords)
            break
        else:
            print("Invalid choice. Please try again.")

def add(passwords):
    website=input("Enter the website: ")
    username=input("Enter the username: ")
    password=input("Enter the password: ")
    passwords.append({"website": website.lower(), "username": username, "password": password})

def view(passwords):
    if not passwords:
        print("No passwords found.")
    else:
        show_website(passwords)
        choice=input("Enter \"all\" to view all password, or enter a website to view the password for that website: ")
        choice=choice.lower()
        if choice=="all":
            for password in passwords:
                print(f"Website: {password['website']}, Username: {password['username']}, Password: {password['password']}")
        else:
            found=False
            for password in passwords:
                if password["website"]==choice:
                    print(f"Website: {password['website']}, Username: {password['username']}, Password: {password['password']}")                    
                    found=True
            if found==False:
                print("No password found for that website.")

def edit(passwords):
    while True:
        print("\n Pick the index of the action:")
        print("3.1 Update password")
        print("3.2 Delete password")
        print("3.3 Back to main menu")
        choice=input("Enter your choice: ")
        if choice=="3.1":
            update(passwords)
        elif choice=="3.2":
            delete(passwords)
        elif choice=="3.3":
            break
        else:
            print("Invalid choice. Please try again.")

def show_website(passwords):
    print("\nList of websites:")
    unreplicated_websites=[]
    for password in passwords:
        if password["website"] not in unreplicated_websites:
            unreplicated_websites.append(password["website"])
            print(password["website"])


def update(passwords):
    show_website(passwords)
    website=input("Enter the website for which to update the password: ")
    website=website.lower()
    print(f"\nList of passwords under the website {website}:")
    found_website=False
    for password in passwords:
        if password["website"]==website:
            print(f"Username: {password['username']}, Password: {password['password']}")
            found_website=True
    if found_website==False:
        print(f"No account found for the website {website}. Try again.")
        return
    
    username=input("Enter the username for which to update the password: ")
    newpassword=input("Enter the new password: ")
    found_username=False
    for password in passwords:
        if password["website"]==website and password["username"]==username:
            password["password"]=newpassword
            print("Password updated successfully.")
            found_username=True
    if found_username==False:
        print(f"No username found for {username}. Try again.")
        return
    return

def delete(passwords):
    show_website(passwords)
    website=input("Enter the website for which to delete the password: ")
    website=website.lower()
    print(f"\nList of passwords under the website {website}:")
    found_website=False
    for password in passwords:
        if password["website"]==website:
            print(f"Username: {password['username']}, Password: {password['password']}")
            found_website=True
    if found_website==False:
        print(f"No account found for the website {website}. Try again.")
        return
    
    username=input("Enter the username for which to delete ")
    found_username=False
    for password in passwords:
        if password["website"]==website and password["username"]==username:
            passwords.remove(password)
            print("Password deleted successfully.")
            found_username=True

    if found_username==False:
        print(f"No username found for {username}. Try again.")

    return

if __name__=="__main__":
    main()