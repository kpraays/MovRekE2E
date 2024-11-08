import mysql.connector
from datetime import datetime

host = "localhost"
port = 3306
user = "root"
password = "temp"
database = "prov"

insert_query = "INSERT INTO reccom (version_number, user_id) VALUES (%s, %s)"
values = (43, 123)


def db_execute(query, values):
    """
        Execute a single query and close the connection.
    """
    try:
        # Connect to MySQL container running on host
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(query, values)

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as exc:
        raise Exception(f"An error occurred: {str(exc)}")

def db_insert(tablename, data):
    if tablename == "reccom":
        query = "INSERT INTO reccom (version_number, user_id) VALUES (%s, %s)"
        values = (data.get("version_number"), data.get("user_id"))
    elif tablename == "tracking":
        query = "INSERT INTO tracking (version_number, data_creation, trained_on, model_rmse) VALUES (%s, %s, %s, %s)"
        values = (data.get("version_number"), data.get("data_creation"), data.get("trained_on"), data.get("model_rmse"))

    db_execute(query, values)


# if __name__ == "__main__":
#     # Get the current UTC timestamp
#     utc_timestamp = datetime.utcnow()

#     db_insert("reccom",{"version_number": 5, "user_id": -99})
#     db_insert("tracking",{"version_number": 5, "data_creation": utc_timestamp, "trained_on": utc_timestamp, "model_rmse":0.45643357355})