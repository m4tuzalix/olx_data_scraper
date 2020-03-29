import sqlite3
from datetime import datetime

class Database():
    def __init__(self):
        self.con = sqlite3.connect('main.db')
        self.cur = self.con.cursor()
        self.now = str(datetime.now().date())

    def db_main(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS links(id INTEGER PRIMARY KEY, link TEXT, date TEXT)")
        self.cur.execute("DELETE FROM links WHERE date != ?", (self.now,))
        self.con.commit()

    def check_db(self,link):
        result = None
        self.cur.execute("SELECT * FROM links WHERE link=?", (link,))
        if self.cur.fetchone():
            result = False
        else:
            result = True
        self.con.commit()
        return result

    def add_links(self,link):
        self.cur.execute("INSERT INTO links VALUES(NULL,?,?)", (link,self.now,))
        self.con.commit()