import plyer
import datetime
import threading
import sqlite3
from time import sleep

def info():
    print("1-Add a reminder.\n2-Remove a reminder.\n3-View all active Reminders.\nQ-Quit")
    a = input()
    try:
        if a.lower() != "q":
            a = int(a)
    except ValueError:
        print("Enter a valid value")
        a = info()
    if a == "q" or 1 <= a <= 3:
        pass
    else:
        print("Enter a valid value")
        a = info()
    return a

def D(a):
    a = a.split("-")
    return datetime.date(int(a[0]), int(a[1]), int(a[2]))

def send_notification(reminder_name,db_file_path):
    plyer.notification.notify(
        title=f"Reminder: {reminder_name}",
        message=f"It's time for '{reminder_name}'",
    )
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE name = ?", (reminder_name,))
    conn.commit()

def check_reminders(db_file_path):
    conn = sqlite3.connect(db_file_path)
    while True:
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reminders")
        for row in cursor.fetchall():
            name, time, date = row
            reminder_date = D(date)
            if reminder_date == current_date and time == current_time:
                send_notification(name,db_file_path)

        sleep(60)  # Sleep for 60 seconds

def View(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders")
    reminders = cursor.fetchall()
    for i, row in enumerate(reminders):
        name, time, date = row
        print(f"{i + 1}) Reminder titled '{name}' is on {date} at {time}.")
    else:
        print("There are no reminders.")

def Add(conn):
    n = input("What is the title: \n")
    t = input("Enter the time (HH:MM): \n")
    d = input("Enter the day: \n")
    m = input("Enter the month: \n")
    y = input("Enter the year: \n")
    Da = f"{y}-{m}-{d}"
    aD = f"{d}-{m}-{y}"

    # Validate the input
    if not n or not t or not d or not m or not y:
        print("Invalid input")
        return

    # Add the reminder to the database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (name, time, date) VALUES (?, ?, ?)", (n, t, Da))
    conn.commit()

    print(f"Reminder titled '{n}' is added on {aD} at {t}")

def Remove(conn):
    t = input("Enter the title of the reminder to be removed:\n")
    a = input("Enter 'CnFrM' to remove the reminder:\n")
    if a == "CnFrM":
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reminders WHERE name = ?", (t,))
        conn.commit()
        print(f"Reminder named '{t}' successfully removed!")
    else:
        print(f"Reminder titled '{t}' removal stopped!")

# Create an SQLite database and table
conn = sqlite3.connect("reminders.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS reminders (name TEXT, time TEXT, date TEXT)")
conn.commit()

# Start

print("Hello, Welcome to the NOTIFIER\n")

# Start the reminder checking thread
reminder_thread = threading.Thread(target=check_reminders, args=("reminders.db",))
reminder_thread.daemon = True
reminder_thread.start()

print("What do you want to do?")
Req = info()

while True:
    if Req == 3:
        View(conn)
    elif Req == 1:
        Add(conn)
    elif Req == 2:
        Remove(conn)
    elif Req == "q" or Req == "Q":
        break
    sleep(1.5)
    print("What do you want to do?")
    Req = info()

# Close the database connection when done
conn.close()