from sqlite3 import Connection
from datetime import datetime

class Database(Connection):
    def __init__(self, **args):
        Connection.__init__(self, 'main.db')
        self.cur = self.cursor()
        self.now = str(datetime.now().date())
    
    def db_main(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS links(id INTEGER PRIMARY KEY, link TEXT UNIQUE, date TEXT)")
        self.cur.execute("DELETE FROM links WHERE date != ?", (self.now,))
        self.commit()
        return True

    def check_db(self,link):
        result = None
        self.cur.execute("SELECT * FROM links WHERE link=?", (link,))
        if self.cur.fetchone():
            result = False
        else:
            result = True
        self.commit()
        return result

    def add_links(self,link):
        self.cur.execute("INSERT INTO links VALUES(NULL,?,?)", (link,self.now,))
        self.commit()