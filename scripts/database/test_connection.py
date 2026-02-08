import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root",
        database="cricsheet_db"
    )

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    print("Connected to MySQL ✅")
    print("Tables:")

    for table in cursor:
        print(table)

    conn.close()

except Exception as e:
    print("Connection Failed ❌")
    print(e)