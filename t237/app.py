import pyodbc
import requests
from datetime import datetime, timedelta
import time

# Database connection (replace with your actual connection details)
conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'  # Use the appropriate driver
            'SERVER=DESKTOP-POD7LTA\\SQLEXPRESS;'  # Replace with your server name
            'DATABASE=test;'  # Replace with your database name
            'UID=sa;'  # Replace with your username
            'PWD=sadguru'  # Replace with your password
        )
def check_and_execute_jobs():
    cursor = conn.cursor()

    # Fetch all active jobs
    cursor.execute("SELECT Id, ProcessUrl, StartTime, EndTime, Interval, TimeOutSec FROM Jobs WHERE IsActive = 1")
    jobs = cursor.fetchall()

    current_time = datetime.now().time()  # Get current time

    for job in jobs:
        job_id, process_url, start_time, end_time, interval, timeout_sec = job
        print(start_time, current_time,end_time)
        # Check if current time is within StartTime and EndTime
        if start_time <= current_time <= end_time:

            # Calculate how many minutes since the start time
            start_time_delta = timedelta(hours=start_time.hour, minutes=start_time.minute)
            current_time_delta = timedelta(hours=current_time.hour, minutes=current_time.minute)
            minutes_since_start = (current_time_delta - start_time_delta).total_seconds() / 60.0

            # If current time aligns with the interval (e.g., every X minutes)
            print(minutes_since_start,interval,minutes_since_start % interval)
            if minutes_since_start % interval == 0:
                print(f"Executing job {job_id}: {process_url}")
                try:
                    # Execute the URL (with timeout)
                    response = requests.get(process_url, timeout=timeout_sec)
                    if response.status_code == 200:
                        print(f"Job {job_id} executed successfully.")
                    else:
                        print(f"Job {job_id} failed with status code {response.status_code}.")
                except requests.exceptions.RequestException as e:
                    print(f"Error executing job {job_id}: {e}")



#check_and_execute_jobs()
