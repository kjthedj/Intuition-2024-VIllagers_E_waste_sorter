import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
pw = "DHRUV0505"  # Replace with your actual password
db = "TEST"  # Replace with your database name

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def create_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def create_table(connection, create_table_query):
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("Table created successfully")
    except Error as err:
        print(f"Error: '{err}'")
        
def read_file_and_insert_data(connection, file_path):
    # Open the file
    with open(file_path, 'r') as file:
        # Read each line in the file
        for line in file:
            try:
                # Parse the line as JSON
                data = json.loads(line)

                # Extracting relevant information
                file_name = data['predictions'][0]['image_path']
                top_class = data['predictions'][0]['top']
                top_confidence = data['predictions'][0]['confidence']

                # SQL query to insert data
                insert_query = f"""
                INSERT INTO data (item_name, class, class_confidence)
                VALUES ('{file_name}', '{top_class}', '{top_confidence}');
                """

                # Execute the query to insert data
                execute_query(connection, insert_query)

            except json.JSONDecodeError:
                print("Error decoding JSON from line:", line)
            except KeyError as e:
                print("Missing key in JSON data:", e)
        

# Path to your predictions.txt file
predictions_file_path = 'predictions.txt'  # Update this with the actual path

# Connect to your database
connection = create_db_connection("localhost", "root", pw, db)

# Read the file and insert data into the database
read_file_and_insert_data(connection, predictions_file_path)

# Close the database connection
connection.close()