from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

pw = "DHRUV0505"  # Replace with your actual password
db = "TEST"  # Replace with your database name

# Function to create a database connection
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
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
    return connection

# Route to fetch data from the database and serve it to HTML template
@app.route('/')
def index():
    # Connect to the database
    connection = create_db_connection("localhost", "root", pw, db)

    # Query to retrieve data from the database
    query = "SELECT class, COUNT(*) AS num_detections FROM data GROUP BY class"

    # Execute the query and fetch all rows
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Close the database connection
    connection.close()

    independent_values = ['57.14%', '93.94%', '100.00%', '100.00%','95.45%']  # Replace with actual values

    return render_template('index.html', data=rows, independent_values=independent_values)    # Pass the data to the HTML template
    # return render_template('index.html', data=rows)

if __name__ == '__main__':
    app.run(debug=True)
