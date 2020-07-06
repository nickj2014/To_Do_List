from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta


def main():
    # Initial database creation
    engine = create_engine("sqlite:///todo.db?check_same_thread=False")
    Base = declarative_base()

    # Base table class to create and update
    class Table(Base):
        __tablename__ = "task"
        id = Column(Integer, primary_key=True)
        task = Column(String, default="default_value")
        deadline = Column(Date, default=datetime.today().date())

        def __repr__(self):
            return self.task

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
        try:
            choice = int(input(">"))
            print()
            if choice == 1:
                todays_tasks(session, Table)
            elif choice == 2:
                weeks_tasks(session, Table)
            elif choice == 3:
                all_tasks(session, Table)
            elif choice == 4:
                missed_tasks(session, Table)
            elif choice == 5:
                enter_task(session, Table)
            elif choice == 6:
                delete_task(session, Table)
            elif choice == 0:
                print("Bye!", end="")
                break
            else:
                print("Input error\n")
        except ValueError:
            print("Input error\n")


def enter_task(session, Table):
    task = input("Enter task:\n")  # User task input
    dl = datetime.strptime(input("Enter deadline as Y-M-D:\n"), "%Y-%m-%d").date()  # User deadline input formatted
    new_row = Table(task=task, deadline=dl)  # Make new row with user inputs
    session.add(new_row)
    session.commit()  # Update table
    print("The task has been added!\n")


def todays_tasks(session, Table):
    rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()  # Get rows of today's date
    count = 1
    print("Today,", datetime.today().day, datetime.today().strftime("%b"))  # Print current date
    if rows:  # If there are rows, print them
        for row in rows:
            print(f"{count}. {row}")
            count += 1
        print()
    else:
        print("Nothing to do!\n")


def weeks_tasks(session, Table):
    rows = session.query(Table).order_by(Table.deadline).all()  # Get rows ordered by deadline
    today = datetime.today()  # Current date for manipulation
    for i in range(7):  # Check each day up to 7 days from today
        empty = True
        count = 1
        next_day = today + timedelta(days=i)  # Get each new day
        print(next_day.strftime('%A'), next_day.day, next_day.strftime('%b'))  # Print new day
        for row in rows:
            if row.deadline == next_day.date():  # Check if any rows match new day
                print(f"{count}. {row}")
                count += 1
                empty = False
        if empty:  # If no tasks printed on current day
            print("Nothing to do!\n")
        else:
            print()


def all_tasks(session, Table):
    rows = session.query(Table).order_by(Table.deadline).all()  # Get rows ordered by deadline
    print("All tasks:")
    count = 0
    if rows:  # If there are tasks in database, print them in order
        for row in rows:
            count += 1
            print(f"{count}. {row} {row.deadline.day} {row.deadline.strftime('%b')}")
        print()
    else:
        print("No current tasks!\n")


def missed_tasks(session, Table):
    # Get rows from db where date is today or before
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    count = 1
    print("Missed tasks:")
    if rows:  # If there are missed tasks, print them
        for row in rows:
            print(f"{count}. {row} {row.deadline.day} {row.deadline.strftime('%b')}")
            count += 1
        print()
    else:
        print("Nothing missed!\n")


def delete_task(session, Table):
    # Get rows from db where date is today or before
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    count = 1
    if rows:  # If there are old tasks, print them
        print("Choose the number of the task you want to delete:")
        for row in rows:  # Print each missed task
            print(f"{count}. {row} {row.deadline.day} {row.deadline.strftime('%b')}")
            count += 1
        remove_row = int(input()) - 1  # Get user input, minus 1 for correct selection
        session.delete(rows[remove_row])  # Delete row user chose
        session.commit()
        print("Task deleted.\n")
    else:
        print("Nothing to delete!\n")


main()
