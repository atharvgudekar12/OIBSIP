import socket
import threading
from datetime import datetime


HOST = "127.0.0.1"
PORT = 5555


# Create server socket
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()


# Connected clients
clients = []
nicknames = []


def get_time():
    return datetime.now().strftime("%H:%M")


def broadcast(message):
    for client in clients:
        try:
            client.send(
                message.encode("utf-8")
            )
        except:
            pass


def send_user_list():
    """Send currently online users to all clients."""

    user_list = ", ".join(nicknames)

    message = f"ONLINE_USERS:{user_list}"

    for client in clients:
        try:
            client.send(
                message.encode("utf-8")
            )
        except:
            pass


def handle_client(client):

    while True:

        try:
            message = client.recv(1024).decode("utf-8")

            if not message:
                break

            index = clients.index(client)
            nickname = nicknames[index]

            current_time = get_time()

            broadcast(
                f"[{current_time}] {nickname}: {message}"
            )

        except:
            break

    # Handle disconnected client
    if client in clients:

        index = clients.index(client)
        nickname = nicknames[index]

        clients.remove(client)
        nicknames.remove(nickname)

        client.close()

        current_time = get_time()

        broadcast(
            f"[{current_time}] {nickname} left the chat."
        )

        # Update online users
        send_user_list()


def receive_connections():

    print(f"Server started on {HOST}:{PORT}")

    while True:

        client, address = server.accept()

        print(f"Connected: {address}")

        try:

            # Receive username
            nickname = client.recv(1024).decode("utf-8").strip()

            # Check empty username
            if not nickname:

                client.send(
                    "ERROR:Username cannot be empty.".encode("utf-8")
                )

                client.close()

                continue

            # Check duplicate username
            if nickname in nicknames:

                client.send(
                    "ERROR:Username already exists.".encode("utf-8")
                )

                client.close()

                print(
                    f"Rejected duplicate username: {nickname}"
                )

                continue

            # Add client
            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname: {nickname}")

            # Send welcome message
            client.send(
                "Connected to the chat server.".encode("utf-8")
            )

            # Notify all users
            current_time = get_time()

            broadcast(
                f"[{current_time}] {nickname} joined the chat!"
            )

            # Send updated online users
            send_user_list()

            # Start client thread
            thread = threading.Thread(
                target=handle_client,
                args=(client,),
                daemon=True
            )

            thread.start()

        except Exception as error:

            print(
                f"Connection error: {error}"
            )

            try:
                client.close()
            except:
                pass


# Start server
receive_connections()