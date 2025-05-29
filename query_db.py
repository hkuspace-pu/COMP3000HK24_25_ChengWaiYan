import sqlite3

# Connect to the database
conn = sqlite3.connect('hashes.db')
cursor = conn.cursor()

# Query the hashes table
cursor.execute("SELECT * FROM hashes;")
rows = cursor.fetchall()

# Print results
if rows:
    for row in rows:
        print(f"File: {row[0]} | Hash: {row[1]}")
else:
    print("No entries found in hashes table.")

# Close connection
conn.close()