import sqlite3


class db:
    def __init__(self, name, name_table, table):
        con = sqlite3.connect(name)
        cur = con.cursor()
        self.name_table = name_table
        self.table = table
        try:
            cur.execute(f"CREATE TABLE {name_table}({table})")
        except:
            pass
        self.cur, self.con = cur, con

    def get_text(self):
        return [*self.cur.execute(f"SELECT * FROM {self.name_table}")]

    def create(self, name, password):
        l = False
        for table in self.get_text():
            if (name, password) == (table[0], table[1]):
                l = True
        if not l:
            dop_text = ""
            for _ in range(len(self.table.split(","))-2):
                dop_text +=",''"

            self.cur.execute(f"INSERT INTO {self.name_table} VALUES ('{name}', '{password}' {dop_text} )")
            self.con.commit()
        else:
            return True

    def remake(self, now_name, now_password, next_name, next_password):
        l = False
        for table in self.get_text():
            if (table[0], table[1]) == (now_name, now_password):
                l = True
                self.cur.execute(f"DELETE FROM {self.name_table} WHERE name='{now_name}' AND password='{now_password}'")
                self.create(next_name, next_password)
                self.con.commit()
        if not l:
            return True

    def spend_message(self, user_name, server_name, server_password, message):

        messages = message +", "+user_name

        for table in self.get_text():
            if (table[0], table[1])==(server_name, server_password):

                messages += "\r"+table[2]
        self.cur.execute(f"UPDATE {self.name_table} SET messages = '{messages}' WHERE name='{server_name}' AND password='{server_password}'")

