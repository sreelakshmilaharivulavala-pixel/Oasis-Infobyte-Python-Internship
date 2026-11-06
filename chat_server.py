
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000

clients = []
clients_lock = threading.Lock()


def send_message(client, message):
    try:
        client.sendall((message + "\n").encode("utf-8"))
    except OSError:
        pass


def broadcast(message, sender=None):

    with clients_lock:
        current_clients = list(clients)

    for client in current_clients:
        if client != sender:
            send_message(client, message)


def handle_client(client, address):

    print(f"Connected: {address}")

    send_message(
        client,
        "Welcome to the Oasis Chat Application!"
    )

    buffer = ""

    try:

        while True:

            data = client.recv(1024)

            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:

                message, buffer = buffer.split("\n", 1)

                message = message.strip()

                if not message:
                    continue

                if message == "/quit":
                    return

                timestamp = datetime.now().strftime("%H:%M:%S")

                formatted_message = (
                    f"[{timestamp}] "
                    f"{address[0]}: {message}"
                )

                print(formatted_message)

                broadcast(
                    formatted_message,
                    sender=client
                )

    except (ConnectionResetError, OSError):

        print(f"Connection lost: {address}")

    finally:

        with clients_lock:

            if client in clients:
                clients.remove(client)

        try:
            client.close()
        except OSError:
            pass

        broadcast(
            f"{address[0]} disconnected."
        )

        print(f"Disconnected: {address}")


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))

    server.listen()

    print("================================")
    print("Oasis Chat Server")
    print("================================")
    print(f"Server running on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("Press Ctrl+C to stop the server.")

    try:

        while True:

            client, address = server.accept()

            with clients_lock:
                clients.append(client)

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:

        print("\nServer shutting down...")

    finally:

        with clients_lock:
            current_clients = list(clients)
            clients.clear()

        for client in current_clients:

            try:
                client.close()
            except OSError:
                pass

        server.close()

        print("Server stopped.")


if __name__ == "__main__":
    start_server()
