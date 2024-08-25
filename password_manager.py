import tkinter as tk
from tkinter import messagebox, filedialog
import random
import csv

# Functionality to generate a random password
def generate_password(length=12):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+="
    password = "".join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Functionality to add a new password
def add_password():
    service = service_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if service and username and password:
        passwords[service] = {'username': username, 'password': password}
        update_password_list()
        clear_entries()
    else:
        messagebox.showwarning("Incomplete Data", "Please fill in all fields.")

# Functionality to clear input fields
def clear_entries():
    service_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Functionality to update the password list in the GUI
def update_password_list():
    password_listbox.delete(0, tk.END)
    for service in passwords:
        password_listbox.insert(tk.END, service)

# Functionality to display selected password details
def show_password():
    selected_service = password_listbox.get(tk.ACTIVE)
    if selected_service:
        credentials = passwords[selected_service]
        messagebox.showinfo(selected_service, f"Username: {credentials['username']}\nPassword: {credentials['password']}")
    else:
        messagebox.showwarning("Selection Error", "Please select a service.")

# Functionality to export passwords to a CSV file
def export_passwords():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Service", "Username", "Password"])
            for service, credentials in passwords.items():
                writer.writerow([service, credentials['username'], credentials['password']])
        messagebox.showinfo("Export Success", "Passwords exported successfully.")

# Functionality to import passwords from a CSV file
def import_passwords():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                passwords[row['Service']] = {'username': row['Username'], 'password': row['Password']}
            update_password_list()
        messagebox.showinfo("Import Success", "Passwords imported successfully.")

# Main GUI window setup
root = tk.Tk()
root.title("Password Manager")

passwords = {}

# Service Name
tk.Label(root, text="Service").grid(row=0, column=0)
service_entry = tk.Entry(root)
service_entry.grid(row=0, column=1)

# Username
tk.Label(root, text="Username").grid(row=1, column=0)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1)

# Password
tk.Label(root, text="Password").grid(row=2, column=0)
password_entry = tk.Entry(root)
password_entry.grid(row=2, column=1)

# Generate Password Button
generate_button = tk.Button(root, text="Generate Password", command=lambda: generate_password(12))
generate_button.grid(row=2, column=2, padx=5)

# Add Password Button
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.grid(row=3, column=1, pady=5)

# Password Listbox
password_listbox = tk.Listbox(root)
password_listbox.grid(row=4, column=0, columnspan=2)

# Show Password Button
show_button = tk.Button(root, text="Show Password", command=show_password)
show_button.grid(row=5, column=1, pady=5)

# Export and Import Buttons
export_button = tk.Button(root, text="Export Passwords", command=export_passwords)
export_button.grid(row=6, column=0, pady=5)

import_button = tk.Button(root, text="Import Passwords", command=import_passwords)
import_button.grid(row=6, column=1, pady=5)

root.mainloop()
