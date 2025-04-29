# -*- coding: utf-8 -*-

import sqlite3

class SqliteDb:
    def __init__(self, name=None):
        self.conn = None
        self.cursor = None
        
        if name:
            self.open(name)
            
    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()
            print(sqlite3.version)
            print("success connection....")
        except sqlite3.Error as e:
            print("Failed connectiong to database....")
            

    # def create_table(self):
    #     c = self.cursor
    #     c.execute("""CREATE TABLE users(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT ,
    #         name TEXT NOT NULL,
    #         year INTEGER,
    #         admin INTEGER)""")
        
 #####################################################             
    #UPDATE    
    def update(self, query, updates):  
        c = self.cursor
        c.execute(query, updates)
        self.conn.commit()
        
    #INSERT    
    def insert(self, query,inserts):  
        c = self.cursor
        c.execute(query, inserts)
        self.conn.commit()
        
    #SELECT    
    def select(self, query):  
        c = self.cursor
        c.execute(query)
        return c.fetchall()
    
    #DELETE
    def delete(self, query):  
        c = self.cursor
        c.execute(query)
        self.conn.commit()
    
    #FIND un seuk enregistrement 
    def find(self, query):  
        c = self.cursor
        c.execute(query)
        return c.fetchall()[0]
    
    #FIND tout les enregistrements 
    def find2(self, query,t1):  
        c = self.cursor
        c.execute(query,t1)
        return c.fetchall()
        
    # def rechercher_dans_base(codeNo):
    # global rs,cnn
    # try:
    #     rs.execute("SELECT * FROM students WHERE code={}".format(codeNo))
    #     return rs.fetchall()[0]
    # except Exception as e:
    #      print(e)
    #      return(False)    
            
#test = SqliteHelper("monApp.db")
#test.create_table()       # on a déja creer la table 
#test.edit("INSERT INTO users (name,year,admin) VALUES ('glot',37,4)")
#print(test.select("SELECT * FROM users"))  # ça marche avec tout les donnees
#print(test.select("SELECT * FROM users")[2][1])
#test.edit("UPDATE users SET name ='barika' WHERE name='tati'")
#print("*"*20)
#print(test.select("SELECT * FROM users")[2][1])