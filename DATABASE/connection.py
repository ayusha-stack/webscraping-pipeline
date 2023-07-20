import psycopg2
from configparser import ConfigParser

class PostgreSQLConnection:
    def __init__(self, config_file="database.ini", section="postgresql"):
        self.config_file = config_file
        self.section = section
        self.connection = None

    def read_config(self):
        config = ConfigParser()
        config.read(self.config_file)

        if config.has_section(self.section):
            self.host = config.get(self.section, "host")
            self.database = config.get(self.section, "database")
            self.user = config.get(self.section, "user")
            self.password = config.get(self.section, "password")
        else:
            raise Exception(
                f'Section {self.section} is not found in the {self.config_file} file.'
            )

    def connect(self):
        try:
            self.read_config()
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to PostgreSQL database.")
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection to PostgreSQL database closed.")
        else:
            print("No active connection to close.")

    def execute_sql(self, sql_query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(sql_query, params)
            else:
                cursor.execute(sql_query)
            self.connection.commit()
            cursor.close()
        except psycopg2.Error as e:
            print("Error executing query:", e)

def execute_sql_file(sql_file):
    with open(sql_file, 'r') as file:
        sql_script = file.read()

    db_connection = PostgreSQLConnection()
    db_connection.connect()

    try:
        cursor = db_connection.connection.cursor()
        cursor.execute(sql_script)
        db_connection.connection.commit()
        print(f"Executed SQL file: {sql_file}")
    except Exception as e:
        print(f"Error executing SQL file '{sql_file}':", e)
    finally:
        db_connection.close()
