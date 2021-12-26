import socket
import json
import threading
import users.main_in_user as user
import os
import copy


class Player:
    def __init__(self, _conn):
        self.conn = _conn
        self.name = None


    def start(self):
        try:
            while True:
                obj = json.loads(self.conn.recv(1024).decode())
                if obj["command"] == "create_user" or obj["command"] == "open_user":
                    answer_obj = user.start(obj)
                    answer = answer_obj["answer"]
                    if answer == "connected" or answer == "user made":
                        self.conn.send(json.dumps(answer_obj).encode())
                        self.name = obj["name"]
                        break
                    else:
                        self.conn.send(json.dumps(answer).encode())
                else:
                    self.conn.send(json.dumps("please chose command: create_user or open_user").encode())
            print(f"{self.name} is logged")
            self.after_logged()
            conn.close()
        except:
            conn.close()

    def after_logged(self):
        while True:
            try:
                obj = json.loads(self.conn.recv(1024).decode())
            except:
                self.conn.close()
                break


            answer_obj = {}

            if obj["path"] == "user":
                answer_obj.update(user.start(obj))

            elif obj["path"].startswith("server-"):
                path = obj["path"][7:]
                b = False
                for name in os.listdir("servers"):
                    if name == path:
                        b = True
                        exec(f"import servers.{path}.main as server\nanswer_obj.update(server.start(obj))")
                if not b:
                    answer_obj["answer"] = "server not found"

            elif obj["path"] == "create":
                if obj["command"] == "create_server":
                    answer_obj.update(copy.copy(obj["server"]))
                else:
                    answer_obj["answer"] = "Error from command in path create"
            else:
                answer_obj["answer"] = "Error from path"

            self.conn.send(json.dumps(answer_obj).encode())

class All_online:
    def __init__(self):
        self.online = {}

    def start_player(self, _conn):
        player = Player(_conn)

        t = threading.Thread(target=player.start)
        t.start()
        t.name = ""
        self.online[t] = player

    def get_online(self):
        names = []
        arr = self.online.copy()
        for t in list(arr.keys()):
            if not t.isAlive():
                del(self.online[t])
            else:
                names.append(self.online[t].name)
        return names


all_online = All_online()

sock = socket.socket()
sock.bind(('localhost', 9090))
sock.listen()
print("start server")
while True:
    conn, adr = sock.accept()

    print('connected: ', adr)
    all_online.start_player(conn)



sock.close()
