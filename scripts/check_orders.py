import sqlite3


connection = sqlite3.connect(
    "data/ecommerce.db"
)

cursor = connection.cursor()

cursor.execute(
    "PRAGMA table_info(orders)"
)

columns = cursor.fetchall()

print("===== ORDERS TABLE =====")

for column in columns:

    print(column)

connection.close()