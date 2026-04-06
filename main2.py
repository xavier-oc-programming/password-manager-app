from tkinter import *
from tkinter import messagebox
import random
import pyperclip  # For reliable clipboard copy
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    # Randomly choose parts of the password
    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    # Insert into entry
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # Copy to clipboard with pyperclip
    pyperclip.copy(password)
    messagebox.showinfo(title="Password Generated", message="Password  copied to clipboard!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().strip()
    email = email_user_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not email or not password:
        messagebox.showwarning(title="Missing Information", message="Please fill in all fields.")
        return

    is_ok = messagebox.askokcancel(
        title=website,
        message=(
            f"Website: {website}\n"
            f"Email: {email}\n"
            f"Password: {password}\n\n"
            "Save to file?"
        )
    )
    if not is_ok:
        return

    new_data = {website: {"email": email, "password": password}}

    # --- Read existing JSON (handle first-run and corrupt JSON) ---
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)              # existing dict
            if not isinstance(data, dict):   # extra guard
                data = {}
    except FileNotFoundError:
        data = {}                            # first run: start fresh
    except json.JSONDecodeError:
        # file exists but is empty/corrupt → start fresh
        data = {}

    # --- Merge new entry INTO existing data ---
    data.update(new_data)

    # --- Write the MERGED dict back (pretty for readability) ---
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)

    # --- Clear fields ---
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    messagebox.showinfo(title="Saved", message=f"Saved credentials for {website}.")

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_entry.get().strip()
    if not website:
        messagebox.showwarning(title="Missing Information", message="Please enter a website to search.")
        return

    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise json.JSONDecodeError("Not a dict", doc="", pos=0)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found (data.json).")
        return
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="Data file is empty or corrupt.")
        return

    creds = data.get(website)
    if not creds:
        messagebox.showinfo(title="Not Found", message=f"No details for '{website}' were found.")
        return

    # Fill entries with found credentials
    email_user_entry.delete(0, END)
    email_user_entry.insert(0, creds.get("email", ""))

    password_entry.delete(0, END)
    password_entry.insert(0, creds.get("password", ""))

    # Offer quick copy to clipboard
    pyperclip.copy(creds.get("password", ""))
    messagebox.showinfo(
        title="Credentials Found",
        message=f"Email: {creds.get('email','')}\nPassword: {creds.get('password','')}copied to clipboard."
    )


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=50)

window.grid_columnconfigure(1, weight=1)

# Logo
image1 = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=image1)
canvas.grid(column=1, row=0, columnspan=2)

# Labels
Label(text="Website:").grid(column=0, row=1, sticky="e")
Label(text="Email/Username:").grid(column=0, row=2, sticky="e")
Label(text="Password:").grid(column=0, row=3, sticky="e")

# Entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2, sticky="we")
website_entry.focus()

email_user_entry = Entry(width=35)
email_user_entry.grid(column=1, row=2, columnspan=2, sticky="we")

password_entry = Entry(width=20)
password_entry.grid(column=1, row=3, sticky="w")

# Buttons
search_button = Button(text="Search", width=20, command=search_password)
search_button.grid(column=2, row=1, sticky="we")

generate_password_button = Button(text="Generate Password", width=20, command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="we")

add_button = Button(text="Add", command=save_password)
add_button.grid(column=1, row=4, columnspan=2, sticky="we")

window.mainloop()