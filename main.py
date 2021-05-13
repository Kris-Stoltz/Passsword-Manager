from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

DARK = '#1a1828'
LIGHT = '#6ac5b6'
RED = '#e8254a'

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH INFO --------------------------------- #


def search_info():
    web_search = website_entry.get()

    if len(web_search) == 0:
        messagebox.showinfo(title='Oops!', message='Please enter a website to search')
    else:
        try:
            with open('passwords.json', 'r') as data_file:
                info = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title='Oops!', message='No Data File Found.')
        except json.decoder.JSONDecodeError:
            messagebox.showinfo(title='Oops!', message='No Data Saved To Data File')
        else:
            if web_search in info:
                email_info = info[web_search]['email']
                password_info = info[web_search]['password']
                messagebox.showinfo(title=web_search,
                                    message=f'Email: {email_info}\nPassword: {password_info}')
            else:
                messagebox.showinfo(title='Oops!', message=f'No details for {web_search} exists. ')


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    web = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        web: {
            'email': email,
            'password': password,
        }
    }

    if (len(web) or len(email) or len(password)) == 0:
        messagebox.showinfo(title='Oops', message='Hey! Looks like you left a field empty.')
    else:
        try:
            with open('passwords.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('passwords.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open('passwords.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50, bg=DARK)
window.resizable(False, False)

canvas = Canvas(width=220, height=200, bg=DARK, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(120, 100, image=img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text='Website:', bg=DARK, fg=RED)
website_label.grid(column=0, row=1)


email_label = Label(text='Email/Username:', bg=DARK, fg=RED)
email_label.grid(column=0, row=2)


password_label = Label(text='Password:', bg=DARK, fg=RED)
password_label.grid(column=0, row=3)


# Entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2, sticky=EW, pady=5)
website_entry.focus()


email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky=EW)
email_entry.insert(0, 'kris.stoltz.ks@gmail.com')


password_entry = Entry()
password_entry.grid(column=1, row=3, sticky=EW)


# Buttons
generate_btn = Button(text='Generate Password', bg=LIGHT, command=generate_password)
generate_btn.grid(column=2, row=3, sticky=EW, pady=2)


add_btn = Button(text='add', width=30, bg=RED, command=save_password)
add_btn.grid(column=1, row=4, columnspan=2, sticky=EW)

search_btn = Button(text='Search', bg=LIGHT, command=search_info)
search_btn.grid(column=2, row=1, sticky=EW, pady=2)

window.mainloop()
