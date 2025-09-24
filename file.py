import pyodbc
import datetime
import os

# SQL Server connection details
server = 'YOUR_SERVER_NAME'      # e.g. 'localhost' or 'SERVER\\INSTANCE'
database = 'YourDatabaseName'
username = 'your_username'
password = 'your_password'



# Backup folder path
backup_dir = r'C:\SQLBackups'

# Create folder if not exists
os.makedirs(backup_dir, exist_ok=True)

# Build backup file name with timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(backup_dir, f"{database}_FULL_{timestamp}.bak")

# SQL Backup command
backup_sql = f"""
BACKUP DATABASE [{database}]
TO DISK = N'{backup_file}'
WITH FORMAT, INIT,
     NAME = N'Full Backup of {database}',
     SKIP, NOREWIND, NOUNLOAD, STATS = 10;
"""

try:
    # Connect to SQL Server
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;UID={username};PWD={password}"
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    print(f"Starting backup of {database} to {backup_file}...")
    cursor.execute(backup_sql)
    print("✅ Backup completed successfully.")

except Exception as e:
    print("❌ Backup failed:", e)

finally:
    if 'conn' in locals():
        conn.close()
