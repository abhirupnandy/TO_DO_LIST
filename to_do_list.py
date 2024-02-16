# IMPORTS
import sqlite3

# library to work with encrypted passwords
import hashlib, getpass

# other libraries
import datetime, time


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
                date TEXT, 
                time TEXT, 
                priority INTEGER,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
            )"""
        )

        self.conn.commit()

    # function to add new task
    def add_task(
        self,
        user_id,
        task,
        date,
        time,
        priority,
    ):
        self.c.execute(
            "INSERT INTO to_do_list (user_id, task, date, time, priority) VALUES (?, ?, ?, ?, ?)",
            (user_id, task, date, time, priority),
        )
        self.conn.commit()

    # function to update task
    # default date and time  = current date and time
    def update_task(
        self,
        task_id,
        task,
        date,
        time,
        priority,
    ):
        self.c.execute(
            "UPDATE to_do_list SET task=?, date=?, time=?, priority=? status='Pending' WHERE id=?",
            (task, date, time, priority, task_id),
        )
        self.conn.commit()

    # function to get all tasks from user with user_id
    def get_tasks(self, user_id):
        self.c.execute("SELECT * FROM to_do_list WHERE user_id=?", (user_id,))
        return self.c.fetchall()

    def get_pending_tasks(self, user_id):
        self.c.execute(
            "SELECT * FROM to_do_list WHERE user_id=? AND status='Pending'", (user_id,)
        )
        return self.c.fetchall()

    def get_completed_tasks(self, user_id):
        self.c.execute(
            "SELECT * FROM to_do_list WHERE user_id=? AND status='Completed'",
            (user_id,),
        )
        return self.c.fetchall()

    def get_overdue_tasks(self, user_id):
        self.c.execute(
            "SELECT * FROM to_do_list WHERE user_id=? AND date < ? AND status='Pending'",
            (user_id, datetime.date.today().strftime("%Y-%m-%d")),
        )
        return self.c.fetchall()

    def get_today_tasks(self, user_id):
        self.c.execute(
            "SELECT * FROM to_do_list WHERE user_id=? AND date = ? AND status='Pending'",
            (user_id, datetime.date.today().strftime("%Y-%m-%d")),
        )
        return self.c.fetchall()

    def get_upcoming_tasks(self, user_id):
        self.c.execute(
            "SELECT * FROM to_do_list WHERE user_id=? AND date > ? AND status='Pending'",
            (user_id, datetime.date.today().strftime("%Y-%m-%d")),
        )
        return self.c.fetchall()

    def complete_task(self, task_id):
        self.c.execute(
            "UPDATE to_do_list SET status='Completed' WHERE id=?", (task_id,)
        )
        self.conn.commit()

    # function to get task with task_id
    def get_task(self, task_id):
        self.c.execute("SELECT * FROM to_do_list WHERE id=?", (task_id,))
        return self.c.fetchone()

    # function to block if user_id is not the owner of the task
    def check_user(self, user_id, task_id):
        self.c.execute("SELECT user_id FROM to_do_list WHERE id=?", (task_id,))
        return self.c.fetchone()[0] == user_id

    def close(self):
        print("\nExiting the application...")
        self.conn.close()
        time.sleep(1)
        print("Goodbye!")


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


# FUNCTIONS
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def main():
    # print the welcome message with a box around it
    try:
        print("+" + "-" * 58 + "+")
        print("|" + " " * 58 + "|")
        print("|" + " " * 10 + "Welcome to the To-Do List Application" + " " * 11 + "|")
        print("|" + " " * 58 + "|")
        print("+" + "-" * 58 + "+")

        # print that the application is loading
        # time.sleep(3)
        print("Loading the databases...")
        # create users and to_do_list objects
        users = Users()
        to_do_list = ToDos()
        USER_ID = None
        # time.sleep(2)
        print("Databases loaded.")
        # time.sleep(1)
        print("+" + "-" * 58 + "+")
        # catch ctrl+c

        print(
            "Please select an option:" "\n1. Login" "\n2. Create new user" "\n3. Exit"
        )
        print("+" + "-" * 58 + "+")
        option = int(input("Option: "))

        # while user_id is not defined, ask for login or create new user
        while USER_ID == None:
            if option == 1:
                # login
                print("+" + "-" * 58 + "+")
                username = input("Username: ")
                # HIDE PASSWORD WHILE TYPING
                password = getpass.getpass("Password: ")
                password = hash_password(password)
                print("+" + "-" * 58 + "+")
                if users.user_exists(username):
                    if users.check_password(username, password):
                        USER_ID = users.c.execute(
                            "SELECT id FROM users WHERE username=?", (username,)
                        ).fetchone()[0]
                        print("Login successful!")
                        print("+" + "-" * 58 + "+")
                        break
                    else:
                        print("Password incorrect!")
                        continue
                else:
                    print("User doesn't exist!")
                    continue
            elif option == 2:
                # create new user
                username = input("Username: ")
                if users.user_exists(username):
                    print("User already exists!")
                    print("+" + "-" * 58 + "+")
                    continue
                else:
                    password = getpass.getpass("Password: ")
                    password = hash_password(password)
                    USER_ID = users.add_user(username, password)
                    print("User created!")
                    print("+" + "-" * 58 + "+")
                    break
            elif option == 3:
                # exit
                to_do_list.close()
                exit()
            else:
                print("Invalid option!")
                print("+" + "-" * 58 + "+")
                continue

        # print the welcome user message
        # time.sleep(1)1

        print("Welcome, " + username + "!")
        print("+" + "-" * 58 + "+")

        # option to view tasks, add new task, update task, delete task or exit
        while True:
            # load all tasks from user with user_id
            tasks = to_do_list.get_tasks(USER_ID)
            print(
                "Please select an option:"
                "\n1. View tasks"
                "\n2. Add new task"
                "\n3. Update task"
                "\n4. Mark task as completed"
                "\n5. View pending tasks"
                "\n6. View completed tasks"
                "\n7. View overdue tasks"
                "\n8. View today's tasks"
                "\n9. View upcoming tasks"
                "\n10. Exit"
            )
            print("+" + "-" * 58 + "+")
            option = int(input("Option: "))

            if option == 1:
                # view tasks
                if len(tasks) == 0:
                    print("No tasks found!")
                    print("+" + "-" * 58 + "+")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task[0]} | Task: {task[2]} | Date: {task[3]} | Time: {task[4]} | Priority: {task[5]} | Status: {task[6]}"
                        )
                        print("+" + "-" * 58 + "+")

            elif option == 2:
                # add new task
                task = input("Task: ")
                date = input("Date (YYYY-MM-DD): ")
                if date == "":
                    print("No date entered!")
                    date = str(datetime.date.today().strftime("%Y-%m-%d"))
                    print(f"Using current date - {date}")
                time = input("Time (HH:MM): ")
                if time == "":
                    print("No time entered!")
                    time = str(
                        (
                            datetime.datetime.now() + datetime.timedelta(hours=1)
                        ).strftime("%H:%M")
                    )
                    print(f"Time set to 1 hour from now - {time}")
                try:
                    priority = int(input("Priority (1-5): "))
                except ValueError:
                    print("Invalid priority!\n Use a number between 1 and 5.")
                    print("+" + "-" * 58 + "+")
                    continue
                to_do_list.add_task(USER_ID, task, date, time, priority)
                tasks = to_do_list.get_tasks(USER_ID)
                print("Task added!")
                print("+" + "-" * 58 + "+")

            elif option == 3:
                # update task
                task_id = int(input("Task ID: "))
                if to_do_list.check_user(USER_ID, task_id):
                    task = input("Task: ")
                    date = input("Date (YYYY-MM-DD): ")
                if date == "":
                    print("No date entered!")
                    date = str(datetime.date.today().strftime("%Y-%m-%d"))
                    print(f"Using current date - {date}")
                time = input("Time (HH:MM): ")
                if time == "":
                    print("No time entered!")
                    time = str(
                        (
                            datetime.datetime.now() + datetime.timedelta(hours=1)
                        ).strftime("%H:%M")
                    )
                    print(f"Time set to 1 hour from now - {time}")
                    try:
                        priority = int(input("Priority (1-5): "))
                    except ValueError:
                        print("Invalid priority!\n Use a number between 1 and 5.")
                        print("+" + "-" * 58 + "+")
                        continue
                    to_do_list.update_task(task_id, task, date, time, priority)
                    tasks = to_do_list.get_tasks(USER_ID)
                    print("Task updated!")
                    print("+" + "-" * 58 + "+")
                else:
                    print("You are not the owner of the task!")
                    print("+" + "-" * 58 + "+")

            elif option == 4:
                # mark task as completed
                task_id = int(input("Task ID: "))
                if to_do_list.check_user(USER_ID, task_id):
                    to_do_list.complete_task(task_id)
                    tasks = to_do_list.get_tasks(USER_ID)
                    print("Task marked as completed!")
                    print("+" + "-" * 58 + "+")
                else:
                    print("You are not the owner of the task!")
                    print("+" + "-" * 58 + "+")

            elif option == 5:
                # view pending tasks
                tasks = to_do_list.get_pending_tasks(USER_ID)
                if len(tasks) == 0:
                    print("No pending tasks found!")
                    print("+" + "-" * 58 + "+")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task[0]} | Task: {task[2]} | Date: {task[3]} | Time: {task[4]} | Priority: {task[5]}"
                        )
                        print("+" + "-" * 58 + "+")

            elif option == 6:
                # view completed tasks
                tasks = to_do_list.get_completed_tasks(USER_ID)
                if len(tasks) == 0:
                    print("No completed tasks found!")
                    print("+" + "-" * 58 + "+")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task[0]} | Task: {task[2]} | Date: {task[3]} | Time: {task[4]} | Priority: {task[5]}"
                        )
                        print("+" + "-" * 58 + "+")

            elif option == 7:
                # view overdue tasks
                tasks = to_do_list.get_overdue_tasks(USER_ID)
                if len(tasks) == 0:
                    print("No overdue tasks found!")
                    print("+" + "-" * 58 + "+")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task[0]} | Task: {task[2]} | Date: {task[3]} | Time: {task[4]} | Priority: {task[5]}"
                        )
                        print("+" + "-" * 58 + "+")

            elif option == 8:
                # view today's tasks
                tasks = to_do_list.get_today_tasks(USER_ID)
                if len(tasks) == 0:
                    print("No tasks for today found!")
                    print("+" + "-" * 58 + "+")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task[0]} | Task: {task[2]} | Date: {task[3]} | Time: {task[4]} | Priority: {task[5]}"
                        )
                        print("+" + "-" * 58 + "+")

            elif option == 9:
                # view upcoming tasks
                tasks = to_do_list.get_upcoming_tasks(USER_ID)
                if len(tasks) == 0:
                    print("No upcoming tasks found!")
                    print("+" + "-" * 58 + "+")
                else:
                    for task in tasks:
                        print(
                            f"ID: {task[0]} | Task: {task[2]} | Date: {task[3]} | Time: {task[4]} | Priority: {task[5]}"
                        )
                        print("+" + "-" * 58 + "+")

            elif option == 10:
                # exit
                to_do_list.close()
                exit()
            else:
                print("Invalid option!")
                print("+" + "-" * 58 + "+")
                continue

    except KeyboardInterrupt:
        print("\nExiting the application...")
        to_do_list.close()
        exit()


# MAIN
if __name__ == "__main__":
    main()
