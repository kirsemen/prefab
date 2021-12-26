import sqlite3


class db:
    def __init__(self, name):
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE users(user_id integer,channel_id integer)")
        except:
            pass
        self.cur, self.con = cur, con

    def get_text(self):
        return [*self.cur.execute("SELECT * FROM users")]

    def create_user(self, user_id, channel_id):
        if not (user_id, channel_id) in self.get_text():
            self.cur.execute(f"INSERT INTO users VALUES ('{user_id}',{channel_id})")
            self.con.commit()
        else:
            return True

    def delete_user(self, user_id):
        users_id = []
        for ids in self.get_text():
            users_id.append(ids[0])
        if user_id in users_id:
            self.cur.execute(f"DELETE FROM users WHERE user_id={user_id}")
            self.con.commit()
        else:
            return True
