# db_initializer.py
import mysql.connector

def create_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS novus")

def create_tables(cursor):
    with open('database/novus.sql', 'r') as file:
        sql_script = file.read()
    cursor.execute(sql_script)

def initialize_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678"
    )

    cursor = connection.cursor()

    try:
        create_database(cursor)
        cursor.execute("USE novus")
        create_tables(cursor)
    except mysql.connector.Error as err:
        print(f"Error al inicializar la base de datos: {err}")
    finally:
        cursor.close()
        connection.close()