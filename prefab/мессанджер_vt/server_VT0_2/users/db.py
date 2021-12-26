import json
import os

class db:
    def __init__(self):
        self.path = "users/users"

    def create_user(self, name, password):
        all_id = ["-1"]
        for name_file in os.listdir(self.path):
            all_id.append(name_file.replace(".db", ""))
        if not self.get_user_by_name(name):
            user = open(self.path + "/" + str(int(all_id[-1])+1) + ".db", "w")
            info = {"name": name,
                    "password": password}
            user.write(json.dumps(info))
            user.close()
            return True
        else:
            return False

    def refract_user(self, name, password, refract_info):

        b, _ = self.open_user(name, password)

        if b:
            id = self.get_user_by_name(name)
            try:
                user = open(self.path + "/" + id + ".db")
                info = json.loads(user.read())
                user.close()
            except:
                return False, "problem with user"
            try:
                user = open(self.path + "/" + id + ".db", "w")
                keys = list(refract_info.keys())
                for key in keys:
                    info[key] = refract_info[key]

                user.write(json.dumps(info))
                user.close()
                return True, info
            except:
                return False, "kwargs error"
        else:
            return False, "Error name or password is not defined"

    def open_user(self, name, password):
        try:
            id = self.get_user_by_name(name)
            user = open(self.path + "/" + id + ".db")
            info = json.loads(user.read())
            user.close()

            if info["name"] == name and info["password"] == password:
                return True, info
            else:
                return False, None
        except:
            return False, None

    def get_user_by_name(self, name):
        try:
            for id in os.listdir(self.path):
                user = open(self.path+"/"+id)
                obj = json.loads(user.read())
                if obj["name"] == name:
                    return id.replace(".db", "")
        except:
            pass