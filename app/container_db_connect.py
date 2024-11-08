import mysql.connector

# MySQL container connection parameters
host = "192.168.96.6"
port = 3306
user = "root"
password = "temp"
database = "prov"

def connect_db():

    try:
        # Connect to MySQL container
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except exc as Exception:
        raise(f"An error occurred while connecting to db from release containers: {str(exc)}")

def db_execute(conn, query, values):
    """
        Execute a single query and close the connection.
    """
    try:
        # Connect to MySQL container running on host
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query, values)

        # Commit the changes
        conn.commit()

        # Close the cursor
        cursor.close()

    except Exception as exc:
        raise Exception(f"An error occurred: {str(exc)}")


def db_insert(conn, tablename, data):
    if tablename == "reccom":
        query = "INSERT INTO reccom (version_number, user_id) VALUES (%s, %s)"
        values = (data.get("version_number"), data.get("user_id"))
    elif tablename == "tracking":
        query = "INSERT INTO tracking (version_number, data_creation, trained_on, model_rmse) VALUES (%s, %s, %s, %s)"
        values = (data.get("version_number"), data.get("data_creation"), data.get("trained_on"), data.get("model_rmse"))

    db_execute(conn, query, values)