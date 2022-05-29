import sqlite3


class DataBase:
    def __init__(self, name):
        self.db = sqlite3.connect(f"{name}")
        cur = self.db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Products (
            id integer primary key,
            product TEXT,
            quanity integer
            )
        """)
        self.db.commit()
        cur.close()

    def read(self):
        cur = self.db.cursor()
        cur.execute("""SELECT * FROM Products""")
        records = cur.fetchall()
        cur.close()
        return records

    def update(self, id, product, quanity):
        id = int(id)
        cur = self.db.cursor()
        cur.execute(f""" UPDATE Products set product="{product}", quanity="{quanity}" WHERE id={id}""")
        self.db.commit()
        cur.close()

    def delete(self, id):
        cur = self.db.cursor()
        cur.execute(f"""DELETE from Products WHERE id={id}""")
        self.db.commit()
        cur.close()

    def insert(self, product, quanity):
        cur = self.db.cursor()
        cur.execute("INSERT INTO Products VALUES (NULL, ?, ?)", (product, quanity))
        self.db.commit()
        cur.close()
