import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox


HOST = "127.0.0.1"
PORT = 5555


class ChatClient:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Chat Application"
        )

        self.root.geometry(
            "750x650"
        )

        self.root.resizable(
            False,
            False
        )

        # Ask username
        self.nickname = simpledialog.askstring(
            "Username",
            "Enter your username:",
            parent=self.root
        )

        if not self.nickname:
            self.root.destroy()
            return

        self.nickname = self.nickname.strip()

        if not self.nickname:
            messagebox.showerror(
                "Username Error",
                "Username cannot be empty."
            )
            self.root.destroy()
            return

        # Create socket
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        try:

            self.client.connect(
                (HOST, PORT)
            )

            # Send username
            self.client.send(
                self.nickname.encode("utf-8")
            )

        except ConnectionRefusedError:

            messagebox.showerror(
                "Connection Error",
                "Server is not running."
            )

            self.root.destroy()
            return

        except Exception as error:

            messagebox.showerror(
                "Connection Error",
                str(error)
            )

            self.root.destroy()
            return

        # Create GUI
        self.create_gui()

        # Start receiving messages
        receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )

        receive_thread.start()

        # Handle window close
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_connection
        )

    def create_gui(self):

        # =========================
        # Title
        # =========================

        title = tk.Label(
            self.root,
            text=f"Chat Application - {self.nickname}",
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=10
        )

        # =========================
        # Online Users
        # =========================

        users_title = tk.Label(
            self.root,
            text="Online Users",
            font=("Arial", 11, "bold")
        )

        users_title.pack(
            pady=(5, 0)
        )

        self.users_list = tk.Label(
            self.root,
            text="Online: ",
            font=("Arial", 10)
        )

        self.users_list.pack(
            pady=5
        )

        # =========================
        # Chat Area
        # =========================

        self.chat_area = tk.Text(
            self.root,
            font=("Arial", 12),
            state="disabled",
            wrap="word"
        )

        self.chat_area.pack(
            padx=15,
            pady=10,
            fill="both",
            expand=True
        )

        # =========================
        # Bottom Frame
        # =========================

        bottom_frame = tk.Frame(
            self.root
        )

        bottom_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        # =========================
        # Message Input
        # =========================

        self.message_entry = tk.Entry(
            bottom_frame,
            font=("Arial", 12)
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        # Enter = Send
        self.message_entry.bind(
            "<Return>",
            self.send_message
        )

        # =========================
        # Send Button
        # =========================

        send_button = tk.Button(
            bottom_frame,
            text="Send",
            font=("Arial", 11, "bold"),
            command=self.send_message
        )

        send_button.pack(
            side="right"
        )

        # Focus message box
        self.message_entry.focus()

    def send_message(self, event=None):

        message = self.message_entry.get().strip()

        if not message:
            return

        try:

            self.client.send(
                message.encode("utf-8")
            )

            # Clear input
            self.message_entry.delete(
                0,
                tk.END
            )

        except Exception as error:

            messagebox.showerror(
                "Send Error",
                str(error)
            )

    def receive_messages(self):

        while True:

            try:

                message = self.client.recv(
                    1024
                )

                if not message:
                    break

                message = message.decode(
                    "utf-8"
                )

                # =========================
                # Server Error
                # =========================

                if message.startswith(
                    "ERROR:"
                ):

                    error_message = message.replace(
                        "ERROR:",
                        "",
                        1
                    )

                    self.root.after(
                        0,
                        self.show_server_error,
                        error_message
                    )

                    return

                # =========================
                # Online Users
                # =========================

                if message.startswith(
                    "ONLINE_USERS:"
                ):

                    users = message.replace(
                        "ONLINE_USERS:",
                        "",
                        1
                    )

                    self.root.after(
                        0,
                        self.update_users,
                        users
                    )

                    continue

                # =========================
                # Normal Chat Message
                # =========================

                self.root.after(
                    0,
                    self.display_message,
                    message
                )

            except:

                break

    def show_server_error(self, error_message):

        messagebox.showerror(
            "Login Error",
            error_message
        )

        self.close_connection()

    def update_users(self, users):

        self.users_list.config(
            text=f"Online: {users}"
        )

    def display_message(self, message):

        self.chat_area.config(
            state="normal"
        )

        self.chat_area.insert(
            tk.END,
            message + "\n"
        )

        self.chat_area.config(
            state="disabled"
        )

        self.chat_area.see(
            tk.END
        )

    def close_connection(self):

        try:
            self.client.shutdown(
                socket.SHUT_RDWR
            )
        except:
            pass

        try:
            self.client.close()
        except:
            pass

        self.root.destroy()


# =========================
# Start Application
# =========================

root = tk.Tk()

app = ChatClient(root)

root.mainloop()