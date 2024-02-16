# IMPORTS
import sqlite3

# library to work with encrypted passwords
import hashlib


# CLASSES
class ToDos:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("to_do_list.db")
        self.c = self.conn.cursor()

        # Read table from database or create it if it doesn't exist
        # Table structure:
        #   id (int) primary key,
        #   user_id (int) foreign key,
        #   task (text),
        #   date (date),
        #   time (time),
        #   priority (int)

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS to_do_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER, 
                task TEXT, 
                date DATE, 
                time TIME, 
                priority INTEGER, 
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
            )"""
        )

        self.conn.commit()

    # function to add new task
    def add_task(self, user_id, task, date, time, priority):
        self.c.execute(
            "INSERT INTO to_do_list (user_id, task, date, time, priority) VALUES (?, ?, ?, ?, ?)",
            (user_id, task, date, time, priority),
        )
        self.conn.commit()

    # function to delete task
    def delete_task(self, task_id):
        self.c.execute("DELETE FROM to_do_list WHERE id=?", (task_id,))
        self.conn.commit()

    # function to update task
    def update_task(self, task_id, task, date, time, priority):
        self.c.execute(
            "UPDATE to_do_list SET task=?, date=?, time=?, priority=? WHERE id=?",
            (task, date, time, priority, task_id),
        )
        self.conn.commit()

    # function to get all tasks from user with user_id
    def get_tasks(self, user_id):
        self.c.execute("SELECT * FROM to_do_list WHERE user_id=?", (user_id,))
        return self.c.fetchall()

    # function to get task with task_id
    def get_task(self, task_id):
        self.c.execute("SELECT * FROM to_do_list WHERE id=?", (task_id,))
        return self.c.fetchone()

    # function to block if user_id is not the owner of the task
    def check_user(self, user_id, task_id):
        self.c.execute("SELECT user_id FROM to_do_list WHERE id=?", (task_id,))
        return self.c.fetchone()[0] == user_id


class Users:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("to_do_list.db")
        self.c = self.conn.cursor()

        # Read table from database or create it if it doesn't exist
        # Table structure:
        #   id (int) primary key,
        #   username (text),
        #   password (text)

        self.c.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, 
                username TEXT, 
                password TEXT
            )"""
        )

        self.conn.commit()

    # function to add new user
    def add_user(self, username, password):
        self.c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        self.conn.commit()

        # return user id
        self.c.execute("SELECT id FROM users WHERE username=?", (username,))
        return self.c.fetchone()[0]

    # function to check if user exists
    def user_exists(self, username):
        self.c.execute("SELECT * FROM users WHERE username=?", (username,))
        # send user id if user exists or None if user doesn't exist
        return self.c.fetchone() != None

    # function to check if password is correct
    def check_password(self, username, password):
        self.c.execute("SELECT password FROM users WHERE username=?", (username,))
        return self.c.fetchone()[0] == password


# VARIABLES


# FUNCTIONS


# MAIN
