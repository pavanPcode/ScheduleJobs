import pyodbc
import configparser

# Initialize the config parser
config = configparser.ConfigParser()
# Read the configuration file
config.read('db_config.ini')

# Get the database credentials
db_config = {
    'DRIVER': config['database']['DRIVER'],
    'SERVER': config['database']['SERVER'],
    'DATABASE': config['database']['DATABASE'],
    'UID': config['database']['UID'],
    'PWD': config['database']['PWD']
}

# db_config = {
#     'DRIVER': '{ODBC Driver 17 for SQL Server}',  # Use the appropriate driver
#     'SERVER': 'DESKTOP-POD7LTA\\SQLEXPRESS',  # Replace with your server name
#     'DATABASE': 'test1',  # Replace with your database name
#     'UID': 'sa',  # Replace with your username
#     'PWD': 'sadguru'  # Replace with your password
# }
def get_data_from_db(query):
    try:
        # Define the connection string (replace with your database details)
        conn = pyodbc.connect(** db_config)

        # Create a cursor object using the connection
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all the results
        rows = cursor.fetchall()

        # Convert the result into a list of dictionaries for easier use
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        # Close the connection
        cursor.close()
        conn.close()
        if len(rows) == 0 or rows == []:
            return {'data': result, "status": False, 'error': 'no data available'}

        return {'data':result,"status":True,'error':[]}

    except pyodbc.Error as e:
        #print(f"Error connecting to database: {e}")
        return {'data':[],"status":False,'error':str(e)}



# data = get_data_from_db()
# print(data)

def update_record_db(query):
    try:
        # Define the connection string (replace with your database details)
        conn = pyodbc.connect(**db_config)
        cursor = conn.cursor()

        #cursor.execute(query, (currenttime, schedule_id,str(apiresp),StatusCode,status))
        cursor.execute(query)

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        return {'data': f"Successfully updated", "status": True, 'error': []}
    except pyodbc.Error as e:
        return {'data': [], "status": False, 'error': str(e)}
