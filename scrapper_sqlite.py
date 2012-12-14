import sqlite3, os.path

location = 'scrapper.db'
table_name = 'scrapper'

def init():    
    global conn
    global c
    conn = sqlite3.connect(location)
    c = conn.cursor()
    create_database()

def create_database():
    sql = 'create table if not exists ' + table_name + '  (date text, url text, content text, filename text) '
    c.execute(sql)
    conn.commit()

def clear_database():
    sql = 'drop table ' + table_name
    c.execute(sql)
    conn.commit()

def insert_record(date, url, content, filename):
    mylist = [date, url, content, filename]
    sql = 'INSERT OR IGNORE INTO ' + table_name + ' (date, url, content, filename) values (?, ?, ?, ?)' 
    c.execute(sql, mylist)
    conn.commit()

def close_database():
    if conn:
        conn.close()

init()
insert_record("12-12-2012", "sdfsdfs", "somethinghere", "url.txt")
