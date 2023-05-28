import sqlite3


class Database:
    # Connect to sqlite3, start session
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    # Create a table
    def create_table(self, table_name, fields):
        self.cursor.execute(f"CREATE TABLE {table_name} ({fields})")
        self.conn.commit()

    # Insert data into a given table
    def insert(self, table_name, data):
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({data})")
        self.conn.commit()

    def add_column(self, table_name, field):
        # Execute ALTER TABLE statement to add a new column
        query = f"ALTER TABLE {table_name} ADD COLUMN {field}"
        self.cursor.execute(query)
        self.conn.commit()

    # Get data from table
    def get_all_data(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        all_data = self.cursor.fetchall()
        return all_data

    # Delete data from a given table given a value from field
    def delete_data(self, table_name, field, data):
        query = f"DELETE FROM {table_name} WHERE {field} = ?"
        self.cursor.execute(query, (data,))
        self.conn.commit()
    # Close session

    def delete_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name} ")
        self.conn.commit()
    def close_connection(self):
        self.conn.close()

#DB = Database("chatbot.db")
#DOG = DB.get_all_data("KB")
#print(DOG)



