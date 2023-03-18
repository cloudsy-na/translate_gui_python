import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS datakamus (id INTEGER PRIMARY KEY, kata char(200), arti char(200), flag integer default Yes, sqltime timestamp default current_timestamp, sqltimeupdate timestamp default current_timestamp)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM datakamus")
        rows = self.cur.fetchall()
        return rows

    def insert(self, kata, arti, flag, sqltime, sqltimeupdate):
        self.cur.execute("INSERT INTO datakamus VALUES (NULL, ?, ?, ?, ?, ?)", (kata, arti, flag, sqltime, sqltimeupdate))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM datakamus WHERE id=?",(id,))
        self.conn.commit()

    def update(self, id, kata, arti, flag, sqltime, sqltimeupdate):
        self.cur.execute("UPDATE datakamus SET kata = ?, arti = ?, flag = ?, sqltime = ?, sqltimeupdate = ? WHERE id = ?",(kata, arti, flag, sqltime, sqltimeupdate, id))
        self.conn.commit() 

    def __del__(self):
        self.conn.close()


# db = Database("test.db")
# db.insert("BL Cotton Gloves","Sarung Tangan Katun BL")
# db.insert("BNC Crimping Tool","Tang Crimping BNC")
# db.insert("BX Protective Eyewear","Kacamata Safety")
# db.insert("Baby Bathtub BAMBINO","Baby Bathtub BAMBINO")
# db.insert("Baby Bathtub LAGOON","Baby Bathtub LAGOON")
# db.insert("Baby Bathtub MELODY","Baby Bathtub MELODY")
# db.insert("Baby Bathtub PARADISE","Baby Bathtub PARADISE")
# db.insert("Back Buttering Trowel","Sendok Semen Bergerigi")
# db.insert("Back Support Belt","Penyangga Punggung")
# db.insert("Backing pads for Angle Grinders","Alas Topang untuk Gerinda Tangan")
# db.insert("Backpack Brush Cutter","Mesin Potong Rumput")
