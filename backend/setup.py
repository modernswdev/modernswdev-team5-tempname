import os
import sqlite3
import csv

DB_PATH = os.environ.get("DATABASE_PATH", "database/service_requests.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def prepare_database():
    connection = get_connection()
    with open("database/database_tables.sql", "r") as schema:
        setup_string = schema.read()

    cursor = connection.cursor()
    cursor.executescript(setup_string)
    connection.commit()
    cursor.close()
    connection.close()


def read_datasets():
    connection = get_connection()
    cursor = connection.cursor()

    with open("datasets/service_requests.csv", newline="\n") as service_requests_file:
        service_requests = csv.reader(service_requests_file, delimiter=",", quotechar="|")
        next(service_requests)

        for row in service_requests:
            status_converted = 0
            if row[3] == "Open":
                status_converted = 0
            elif row[3] == "In Progress":
                status_converted = 1
            elif row[3] == "Resolved" or row[3] == "Closed":
                status_converted = 2

            priority_converted = 0.0
            if row[4] == "Low":
                priority_converted = 2.5
            elif row[4] == "Medium":
                priority_converted = 5.0
            elif row[4] == "High":
                priority_converted = 7.5

            cursor.execute(
                """
                INSERT OR IGNORE INTO Requests
                (RequestID, RequestTitle, RequestBody, RequestStatus, RequestPriority, RequestCreatorID, RequestCreateDate, RequestModifyDate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (int(row[0]), row[1], row[2], status_converted, priority_converted, int(row[7]), row[5], row[6]),
            )

            if row[8] != "":
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO Assignees (AssigneeRequestID, AssigneeHandlerID)
                    VALUES (?, ?)
                    """,
                    (int(row[0]), int(row[8])),
                )

    with open("datasets/users.csv", newline="\n") as users_file:
        users = csv.reader(users_file, delimiter=",", quotechar="|")
        next(users)

        for row in users:
            role_converted = 0
            if row[4] == "user":
                role_converted = 1
            elif row[4] == "staff":
                role_converted = 2
            elif row[4] == "admin":
                role_converted = 3

            cursor.execute(
                """
                INSERT OR IGNORE INTO Users
                (UserID, UserFirstName, UserLastName, UserEmail, UserPassword, UserRole, UserCreateDate)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (int(row[0]), row[1], row[2], row[3], "password" + str(row[0]), role_converted, row[5]),
            )

    connection.commit()
    cursor.close()
    connection.close()


def database_ready():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'"
    )
    has_users = cursor.fetchone() is not None

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Requests'"
    )
    has_requests = cursor.fetchone() is not None

    users_count = 0
    requests_count = 0
    if has_users:
        cursor.execute("SELECT COUNT(*) FROM Users")
        users_count = int(cursor.fetchone()[0])
    if has_requests:
        cursor.execute("SELECT COUNT(*) FROM Requests")
        requests_count = int(cursor.fetchone()[0])

    connection.close()
    return has_users and has_requests and users_count > 0 and requests_count > 0


def initialize_database_if_needed():
    if database_ready():
        return

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    prepare_database()
    read_datasets()


initialize_database_if_needed()

if __name__ == "__main__":
    print("Database prepared and datasets loaded.")
