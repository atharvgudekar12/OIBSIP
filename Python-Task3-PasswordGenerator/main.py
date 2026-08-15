import tkinter as tk
from tkinter import messagebox

from password_generator import generate_password


def generate():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 4."
            )
            return

        password = generate_password(length)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

        strength_label.config(
            text="Password generated successfully!",
            fg="green"
        )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )


def copy_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    strength_label.config(
        text="Password copied to clipboard!",
        fg="blue"
    )


# Main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x400")
root.resizable(False, False)


# Title
title_label = tk.Label(
    root,
    text="Password Generator",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=25)


# Length
length_label = tk.Label(
    root,
    text="Password Length",
    font=("Arial", 12)
)
length_label.pack()

length_entry = tk.Entry(
    root,
    width=25,
    font=("Arial", 12),
    justify="center"
)
length_entry.pack(pady=8)


# Generate button
generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate,
    font=("Arial", 12)
)
generate_button.pack(pady=15)


# Password
password_label = tk.Label(
    root,
    text="Generated Password",
    font=("Arial", 12)
)
password_label.pack()

password_entry = tk.Entry(
    root,
    width=35,
    font=("Arial", 12),
    justify="center"
)
password_entry.pack(pady=8)


# Copy button
copy_button = tk.Button(
    root,
    text="Copy Password",
    command=copy_password,
    font=("Arial", 12)
)
copy_button.pack(pady=10)


# Status
strength_label = tk.Label(
    root,
    text="Enter a length and generate a password.",
    font=("Arial", 11)
)
strength_label.pack(pady=15)


root.mainloop()