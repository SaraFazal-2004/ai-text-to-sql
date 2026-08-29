import sqlite3

DATABASE_PATH = "data/ecommerce.db"


def get_database_schema():

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    schema = {}

    for (table_name,) in tables:

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        schema[table_name] = []

        for column in columns:

            column_info = {
                "name": column[1],
                "type": column[2],
                "primary_key": bool(column[5])
            }

            schema[table_name].append(column_info)

    connection.close()

    return schema


def print_schema(schema):

    print("\n========== DATABASE SCHEMA ==========\n")

    for table_name, columns in schema.items():

        print(f"TABLE: {table_name}")

        for column in columns:

            pk = " PRIMARY KEY" if column["primary_key"] else ""

            print(
                f"  - {column['name']} "
                f"({column['type']}){pk}"
            )

        print()


if __name__ == "__main__":

    database_schema = get_database_schema()

    print_schema(database_schema)