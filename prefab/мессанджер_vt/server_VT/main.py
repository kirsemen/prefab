import socket
import db


users = db.db("users.db", "users", "name text, password text")
servers = db.db("servers.db", "servers", "name text, password text, messages text")

sock = socket.socket()
sock.bind(('localhost', 9090))
sock.listen(10)
print(users.get_text())
print(servers.get_text())
servers.create("semen", "semen")

def remake_message(message):
    try:
        message = b"".join(message.split(b",close"))
        arr = eval(message)
        # error_marks = [",", "]", "[", "{", "}", "/", "\\", " ", "-", "=", "+", "*",
        #                "&", "^", "%", "$", "#", "@", "!", "(", ")", "|", "<", ">", "~"]
        # error = False
        # for mark in error_marks:
        #     error = ("".join(arr[0].split(mark)) != arr[0] or
        #              "".join(arr[1].split(mark)) != arr[1] or
        #              error)
        # error = (error or arr[0] == "" or arr[1] == "")
        # if error:
        #     return b"Error special character was used in name or password"

        if arr[2] == "open_user":
            if (arr[0], arr[1]) in users.get_text():
                return b"connected"
            else:
                return b"Error name or password is not defined"
        elif arr[2] == "create_user":
            if len(arr[0]) >= 3 and len(arr[1]) >= 3:
                if users.create(arr[0], arr[1]):
                    return b"user is already done"
                else:
                    print(users.get_text())
                    return b"user made"
            else:
                return b"name or password is very small"
        elif arr[2].startswith("create_server: "):
            text = arr[2][15:]
            name_server = text.split(", ")[0]
            password_server = text.split(", ")[1]
            if (arr[0], arr[1]) in users.get_text():
                if len(name_server) >= 3 and len(password_server) >= 3:
                    if servers.create(name_server, password_server):
                        return b"server is already done"
                    else:
                        print(servers.get_text())
                        return b"server made"
                else:
                    return b"name or password is very small"
            else:
                return b"Error name or password is not defined"
        elif arr[2].startswith("open_server: "):
            text = arr[2][13:]
            name_server = text.split(", ")[0]
            password_server = text.split(", ")[1]

            if (arr[0], arr[1]) in users.get_text():
                l =False
                for server in servers.get_text():
                    if (name_server, password_server) == (server[0], server[1]):
                        l = True
                        return f"{server[2]}".encode("utf-8")
                if not l:
                    return b"Error servers is not defined"
            else:
                return b"Error name or password is not defined"
        elif arr[2].startswith("spend_message: "):

            text = arr[2][15:]
            name_server = text.split(", ")[0]
            password_server = text.split(", ")[1]
            message = ", ".join(text.split(", ")[2:])
            if (arr[0], arr[1]) in users.get_text():
                servers.spend_message(arr[0], name_server, password_server, message)
                return b"message is open"
            else:
                return b"Error name or password is not defined"

        else:
            return b"command is not defined"
    except:
        return b"Error"
    return b""


while True:
    conn, addr = sock.accept()

    print('connected:', addr)

    mes = b""
    x = 1
    while x:
        conn.settimeout(3)
        try:
            data = conn.recv(1024)
        except:
            conn.close()
            break

        mes += data
        if x == 1 and data.endswith(b"],close"):
            conn.send(remake_message(mes))
        else:
            conn.send(b"Error")
            break

        x += 1
    print("break")

sock.close()
