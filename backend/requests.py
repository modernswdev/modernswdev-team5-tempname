import sqlite3
import csv

DB_PATH = "database/service_requests.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

def validate_credentials(email, password):
    connection = get_connection()
    cursor = connection.cursor()

    result = cursor.execute(
        """
        SELECT UserRole
        FROM Users
        WHERE Users.UserEmail = ? AND Users.UserPassword = ?
        """,
        (email, password)
    )

    fetched = result.fetchone()

    connection.close()

    if fetched is None:
        return 0
    else:
        return fetched[0]

def get_user_id(email, password):
    connection = get_connection()
    cursor = connection.cursor()

    result = cursor.execute(
        """
        SELECT UserID
        FROM Users
        WHERE Users.UserEmail = ? AND Users.UserPassword = ?
        """,
        (email, password)
    )

    fetched = result.fetchone()

    connection.close()

    if fetched is None:
        return 0
    else:
        return fetched[0]


def view_requests(requester_email, requester_password):
    if validate_credentials(requester_email, requester_password) < 1:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT RequestID, RequestTitle, RequestStatus, RequestCreateDate FROM Requests")
    rows = cursor.fetchall()

    print("Request List")
    print("===================")

    for row in rows:
        print("-------------------")
        print("id:", row[0])
        print("title:", row[1])
        print("status:", status_int_to_str(int(row[2])))
        print("created_at:", row[3])

    conn.close()


def create_request(title, body, priority, requester_email, requester_password):
    if validate_credentials(requester_email, requester_password) < 1:
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Requests (RequestTitle, RequestBody, RequestPriority, RequestCreatorID)
        VALUES (?, ?, ?, ?)
        """,
        (title, body, priority, get_user_id(requester_email, requester_password))
    )

    conn.commit()
    conn.close()

    print("Request created successfully")


def update_status(request_id, new_status, requester_email, requester_password):
    if validate_credentials(requester_email, requester_password) < 2:
        return False

    conn = get_connection()
    cursor = conn.cursor()

    # I have changed this to have custom error handling, for some reason pytest cannot
    # understand this function very well. - Matthew Ingram

    try:
        cursor.execute(
            "UPDATE Requests SET RequestStatus = ? WHERE RequestID = ?",
            (new_status, request_id)
        )
    except:
        conn.close()
        return False
    else:
        conn.commit()
        conn.close()
        print("Status updated successfully")
        return True
    # End of my changes here. - Matthew Ingram

def view_request_details(request_id):
    # No need to validate credentials, this function is called from another. - Matthew Ingram

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT RequestID, RequestTitle, RequestBody, RequestPriority, RequestStatus, RequestCreateDate, RequestModifyDate
        FROM Requests
        WHERE Requests.RequestID = ?
        """,
        (request_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        print("\nRequest Details")
        print("==========================")
        print(f"ID          : {row[0]}")
        print(f"Title       : {row[1]}")
        print(f"Description : {row[2]}")
        print(f"Priority    : {row[3]}")
        print(f"Status      : {status_int_to_str(int(row[4]))}")
        print(f"Created At  : {row[5]}")
        print(f"Updated At  : {row[6]}")
        print("==========================\n")
    else:
        print(f"\nNo request found with ID {request_id}.\n")


def open_request_details(requester_email, requester_password):
    if validate_credentials(requester_email, requester_password) < 2:
        return
        
    request_id = input("Enter request ID to view details: ")

    try:
        request_id = int(request_id)
        view_request_details(request_id)
    except ValueError:
        print("Invalid ID. Please enter a number.")


def sort_by_priority(requester_email, requester_password):
    if validate_credentials(requester_email, requester_password) < 1:
        return
        
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT RequestID, RequestTitle, RequestPriority, RequestStatus FROM Requests ORDER BY Requests.RequestPriority"
    )

    rows = cursor.fetchall()

    print("Sorted by priority")
    print("===================")

    for row in rows:
        print(row)

    conn.close()


def filter_by_status(status_value, requester_email, requester_password):
    if validate_credentials(requester_email, requester_password) < 1:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT RequestID, RequestTitle, RequestPriority, RequestStatus FROM Requests WHERE Requests.RequestStatus = ?",
        (status_value,)
    )

    rows = cursor.fetchall()

    print(f"Filtered by status = {status_int_to_str(int(status_value))}")
    print("===================")

    for row in rows:
        print(row)

    conn.close()
    return len(rows)  # Added for unit testing. - Matthew Ingram


def status_int_to_str(status_int):
    if status_int == 0:
        return "Open"
    elif status_int == 1:
        return "In Progress"
    elif status_int == 2:
        return "Resolved"

def role_int_to_str(role_int):
    if role_int == 0:
        return "No Login"
    elif role_int == 1:
        return "User"
    elif role_int == 2:
        return "Staff"
    elif role_int == 3:
        return "Admin"

# Prepare database. - Matthew Ingram
def prepare_database():
    connection = get_connection()
    with open("database/database_tables.sql", "r") as schema:
        setup_string = schema.read()
    cursor = connection.cursor()
    cursor.executescript(setup_string)
    connection.commit()
    cursor.close()
    connection.close()

# Prepare both datasets. - Matthew Ingram
def read_datasets():
    connection = get_connection()
    cursor = connection.cursor()
    with open("datasets/service_requests.csv", newline = "\n") as service_requests_file:
        service_requests = csv.reader(service_requests_file, delimiter = ",", quotechar = "|")
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
                INSERT INTO Requests (RequestID, RequestTitle, RequestBody, RequestStatus, RequestPriority, RequestCreatorID, RequestCreateDate, RequestModifyDate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (int(row[0]), row[1], row[2], status_converted, priority_converted, int(row[7]), row[5], row[6])
            )
            connection.commit()

            if (row[8] != ""):
                cursor.execute(
                    """
                    INSERT INTO Assignees (AssigneeRequestID, AssigneeHandlerID)
                    VALUES (?, ?)
                    """,
                    (int(row[0]), int(row[8]))
                )
                connection.commit()

    with open("datasets/users.csv", newline = "\n") as users_file:
        users = csv.reader(users_file, delimiter = ",", quotechar = "|")
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
                INSERT INTO Users (UserID, UserFirstName, UserLastName, UserEmail, UserPassword, UserRole, UserCreateDate)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (int(row[0]), row[1], row[2], row[3], "password" + str(row[0]), role_converted, row[5])
            )
            connection.commit()
    cursor.close()
    connection.close()


prepare_database()
read_datasets()
# End of my addition. - Matthew Ingram

if __name__ == "__main__":
    email, password = input("Please input your user email, followed by your user password: ").split()

    print("1. View requests")
    view_requests(email, password)

    print("\n2. Sort by priority")
    sort_by_priority(email, password)

    print("\n3. Filter by status = In Progress")
    filter_by_status(1, email, password)
    
    print("\n4. Open request details")
    open_request_details(email, password)