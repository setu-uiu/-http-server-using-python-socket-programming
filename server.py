import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print("Server running...")
print("Visit http://localhost:8080")

while True:
    client, address = server.accept()

    try:
        request = client.recv(1024).decode()

        print("Request received:")
        print(request)

        if not request:
            client.close()
            continue

        path = request.split()[1]

        if path == "/":
            filename = "index.html"
        else:
            filename = path[1:]

        with open(filename, "r") as file:
            content = file.read()

        response = "HTTP/1.0 200 OK\r\n\r\n"
        response += content

    except FileNotFoundError:
        response = """HTTP/1.0 404 NOT FOUND\r\n\r\n
<html>
<body>
<h1>404 Not Found</h1>
</body>
</html>
"""

    except Exception as e:
        print("Error:", e)
        response = "HTTP/1.0 500 INTERNAL SERVER ERROR\r\n\r\n"

    client.send(response.encode())
    client.close()