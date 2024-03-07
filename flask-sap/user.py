import sqlite3
import logging as log

log.basicConfig(filename='record.log', level=log.DEBUG,
                format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')


def create_table_user():
    create_table_query = '''
         CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email text UNIQUE,
                password text NOT NULL);    
    '''
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        print("connection made")
        cursor.execute(create_table_query)
        conn.commit()
    except sqlite3.Error as error:
        log.warning('Warning level log')
        print("error while creating Table", error)

    finally:
        cursor.close()
        conn.close()


def insert_default_users():
    data = [
        ("admin", "admin@test.com", "password"),
        ("user", "user@test.com", "123456"),
        ("guest", "guest@test.com", "qwerty")]

    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        print("connection made inserting users")
        cursor.executemany(
            "INSERT INTO users (name,email,password) VALUES(?,?,?)", data)
        print("default users entered")
        log.info("default users created")
        conn.commit()
    except sqlite3.Error as error:
        print("error while executing query", error)
    finally:
        cursor.close()
        conn.close()


def insert_users(data):
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        print("connection made inserting users")
        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES(?,?,?)", data)
        print("user entered")
        conn.commit()
    except sqlite3.Error as error:
        print("error while executing query", error)
    finally:
        cursor.close()
        conn.close()


def get_user_email(email):
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        print("Connected to database")
        sql_select_query = """select * from users where email =? """
        cursor.execute(sql_select_query, (email,))
        records = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The connection is closed")
        return records


def get_user_name(name):
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        print("Connected to database")
        cursor.execute("SELECT * FROM users WHERE name = '%s'" % (name))
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
        return []
    finally:
        if conn:
            conn.close()
            print("The connection is closed")


__all__ = ['create_table_user', 'insert_default_users', 'get_user_name']
