import mysql.connector
import pytest

# Configuration details for MySQL connection
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'T6ADZUsoavQjl1g/zmiv4TGvgiSG3mrB',  # Replace with your MySQL password
}

DATABASE_NAME = 'test_db'
USERS_TABLE = 'users'
ORDERS_TABLE = 'orders'


@pytest.fixture(scope="module")
def mysql_connection():
    """Fixture to connect to MySQL server."""
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    yield conn
    conn.close()


@pytest.fixture(scope="module")
def cursor(mysql_connection):
    """Fixture to get a cursor from the MySQL connection."""
    cursor = mysql_connection.cursor()
    yield cursor
    cursor.close()


@pytest.fixture(scope="module", autouse=True)
def setup_database(mysql_connection, cursor):
    """Fixture to create a database before running tests and drop it afterward."""
    # Create the database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cursor.execute(f"USE {DATABASE_NAME}")
    mysql_connection.commit()  # Commit after creating database

    yield  # This allows the test to run

    # Cleanup: Drop the database after the tests run
    cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
    mysql_connection.commit()  # Commit after dropping database


def create_users_table(cursor):
    """Function to create the 'users' table."""
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            age INT
        )
    """)


def create_orders_table(cursor):
    """Function to create the 'orders' table."""
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {ORDERS_TABLE} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount DECIMAL(10, 2),
            order_date DATE,
            FOREIGN KEY (user_id) REFERENCES {USERS_TABLE}(id)
        )
    """)


def test_create_users_table(cursor):
    """Test creating the users table."""
    cursor.execute(f"USE {DATABASE_NAME}")
    create_users_table(cursor)

    # Verify 'users' table exists
    cursor.execute(f"SHOW TABLES LIKE '{USERS_TABLE}'")
    users_table_exists = cursor.fetchone()
    assert users_table_exists is not None, f"Table {USERS_TABLE} does not exist."


def test_create_orders_table(cursor):
    """Test creating the orders table."""
    cursor.execute(f"USE {DATABASE_NAME}")
    create_orders_table(cursor)

    # Verify 'orders' table exists
    cursor.execute(f"SHOW TABLES LIKE '{ORDERS_TABLE}'")
    orders_table_exists = cursor.fetchone()
    assert orders_table_exists is not None, f"Table {ORDERS_TABLE} does not exist."


def test_insert_sample_data(cursor, mysql_connection):
    """Test inserting sample data into the tables."""
    cursor.execute(f"USE {DATABASE_NAME}")

    # Insert data into 'users' table
    cursor.execute(f"""
        INSERT INTO {USERS_TABLE} (name, email, age) 
        VALUES ('John Doe', 'john.doe@example.com', 30),
               ('Jane Smith', 'jane.smith@example.com', 25),
               ('Alice Johnson', 'alice.johnson@example.com', 35)
    """)

    # Insert data into 'orders' table (assuming the 'users' table has auto-increment IDs starting from 1)
    cursor.execute(f"""
        INSERT INTO {ORDERS_TABLE} (user_id, amount, order_date)
        VALUES (1, 100.50, '2024-10-01'),
               (2, 200.00, '2024-10-10'),
               (3, 150.75, '2024-10-12')
    """)

    mysql_connection.commit()  # Commit after inserting data


def test_verify_data(cursor):
    """Test verifying that the sample data was inserted correctly."""
    cursor.execute(f"USE {DATABASE_NAME}")

    # Check data in 'users' table
    cursor.execute(f"SELECT * FROM {USERS_TABLE}")
    users = cursor.fetchall()
    assert len(users) == 3, "There should be 3 users inserted."

    # Check data in 'orders' table
    cursor.execute(f"SELECT * FROM {ORDERS_TABLE}")
    orders = cursor.fetchall()
    assert len(orders) == 3, "There should be 3 orders inserted."

    # Validate specific data (for example, check first user's name)
    cursor.execute(f"SELECT name FROM {USERS_TABLE} WHERE id = 1")
    user_name = cursor.fetchone()[0]
    assert user_name == 'John Doe', "The first user's name should be 'John Doe'."

    # Validate specific order (for example, check the order amount for the first order)
    cursor.execute(f"SELECT amount FROM {ORDERS_TABLE} WHERE id = 1")
    order_amount = cursor.fetchone()[0]
    assert order_amount == 100.50, "The first order's amount should be 100.50."
