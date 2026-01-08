
import sqlite3
import json

class Database:
    def __init__(self, db):
        self.conn=sqlite3.connect("journey.db")
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS study "
                    "")
        self.conn.commit()