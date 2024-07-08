import pickle
import tkinter as tk 
from tkinter import messagebox
from cryptography.fernet import Fernet 

password = "Default"

def generate_key():
    return Fernet.generate_key()

def save_passwords(passwords, filename='passwords.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(passwords, f)

def load_passwords(filename='passwords.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

def encrypt_password(key, password):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def save_key(key, filename='key.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(key, f)

def load_key(filename='key.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

passwords = load_passwords()

def add_password():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if service and username and password:
        encrypted_password = encrypt_password(key, password)
        passwords[service] = {'username':username, 'password':encrypted_password}
        save_passwords(passwords)
        messagebox.showinfo('Success', f'Password for {service} added successfully')
    else:
        messagebox.showerror('Error', 'Please fill all the fields')

def get_password():
    service = service_entry.get()
    if service in passwords:
        encrypted_password = passwords[service]['password']
        decrypted_password = decrypt_password(key, encrypted_password)
        messagebox.showinfo("Password", f"Username: {passwords[service]['username']}\nPassword: {decrypted_password}")
    else:
        messagebox.showerror('Error', f'No password saved for {service}')

key = load_key()
if key is None:
    key = generate_key()
    save_key(key)

instructions = '''To add password fill all the fields and press "Add Password"
To view password, enter Account Name and press "Get Password"'''
signature = "Made by: Alejandra Arias"

window = tk.Tk()
window.title('Password Manager')
window.configure(bg="purple")

window.resizable(False, False)

center_frame = tk.Frame(window, bg="#d3d3d3")
center_frame.pack(pady=10,padx=10)
center_frame.grid(row=0, column=0)

instruction_label = tk.Label(center_frame, text=instructions, bg="#d3d3d3", fg="white")
instruction_label.grid(row=0, column=1, columnspan=2, pady=5, padx =10)

service_label = tk.Label(center_frame, text="Account:", bg="#d3d3d3")
service_label.grid(row=1, column=0, padx=10, pady=5)
service_entry = tk.Entry(center_frame)
service_entry.grid(row=1, column=1, padx=10, pady=5)

username_label = tk.Label(center_frame, text="Username:", bg="#d3d3d3")
username_label.grid(row=2, column=0, padx=10, pady=5)
username_entry = tk.Entry(center_frame)
username_entry.grid(row=2, column=1, padx=10, pady=5)

password_label = tk.Label(center_frame, text="Password:", bg="#d3d3d3")
password_label.grid(row=3, column=0, padx=10, pady=5)
password_entry = tk.Entry(center_frame, show="*")
password_entry.grid(row=3, column=1, padx=10, pady=5)


add_button = tk.Button(center_frame, text="Add Password", command=add_password, height=1, width=10)
add_button.grid(row=5, column=4, padx=10, pady=5)

get_button = tk.Button(center_frame, text="Get Password", command=get_password, height=1, width=10)
get_button.grid(row=6, column=4, padx=10, pady=5)

signature_label = tk.Label(center_frame, text=signature, bg="#d3d3d3")
signature_label.grid(row=7, column=1, padx=5, pady=5)


window.mainloop()