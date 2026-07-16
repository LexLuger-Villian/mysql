import mysql.connector
from mysql.connector import Error

# Database connection configuration

db_config = {
        "host": "localhost",
        "user": "app_user_ro", #MySQL user
        "password": "password123", #MySQL password
        "database": "my_app_db"
}

def get_connection():
    """Estabilishes and returns a database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f" Error connection to MySQL: {e}")
        return None

def create_user(name, email, age):
    """C - Create a new user in the database."""
    connection = get_connection()
    if not connection:
        return

    query = "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)"
    values = (name, email, age)

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        print(f" User '{name}' added successfully! ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Failed ot create user: {e}")
    finally:
        cursor.close()
        connection.close()

def read_users():
    """R - Read and display all users from the database."""
    connection = get_connection()
    if not connection:
        return

    query = "SELECT id, name, email, age FROM users"

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            print("\n No users found in the database.")
            return

        print("\n--- Current Users List ---")
        for row in records:
            print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Age: {row[3]}")
        print("--------------------------")
    except Error as e:
        print(f"Failed to read data: {e}")
    finally:
        cursor.close()
        connection.close()


def update_user(user_id, name, email, age):
    """U - Update an existing user's details by ID."""
    connection = get_connection()
    if not connection:
        return

    query = "UPDATE users SET name = %s, email = %s, age = %s WHERE ID = %s"
    values = (name, email, age, user_id)

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()

        if cursor.rowcount == 0:
            print(f"No user found with ID {user_id}.")
        else:
            print(f"User ID {user_id} updated successfully!")
    except Error as e:
        print(f"Failed to update user: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_user(user_id):
    """D - Delete a user record by ID."""
    connection = get_connection()
    if not connection:
        return

    query = "DELETE FROM users WHERE id = %s"

    try:
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            print(f"No user found with ID {user_id}.")
        else:
            print(f"User ID {user_id} deleted successfully!")
    except Error as e:
        print(f"Failed to delete user: {e}")
    finally:
        cursor.close()
        connection.close()


def menu():
    """Interactive Command Line Menu Interface."""
    while True:
        print("/n---- Python MySQL CRUD App ====")
        print("1. Create User")
        print("2. Read All Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            name = input("Enter name: ")
            email = input("Enter email: ")
            age = input("Enter age: ")
            create_user(name, email, int(age) if age.isdigit() else None)

        elif choice == '2':
            read_users()

        elif choice == '3':
            user_id = input("Enter User ID to update: ")
            if user_id.isdigit():
                name = input("Enter new Name: ")
                email = input("Enter new email: ")
                age = input("Enter new age: ")
                update_user(int(user_id), name, email, int(age) if age.isdigit() else None)
            else:
                print("Invalid User ID.")

        elif choice == '4':
            user_id = input("Enter User ID to delete: ")
            if user_id.isdigit():
                delete_user(int(user_id))
            else:
                print("Invalid User ID.")

        elif choice == '5':
            print("Exiting program. Goodbuy!")
            break
        else:
            print("Invalid selection. Please enter 1-5.")

if __name__ == "__main__":
    menu()

