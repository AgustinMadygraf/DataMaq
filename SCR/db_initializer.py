# db_initializer.py
import mysql.connector
from logs.config_logger import configurar_logging

logger = configurar_logging()


def create_database():
    logger.info("creando la base de datos") 
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678"
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS novus")
    logger.info("base de datos 'novus' creada con éxito")

def create_tables(cursor, tabla):
    if tabla == 'registros_modbus':
        with open('database/registros_modbus_1.sql', 'r') as file:
            print("creando tabla registros_modbus")
            sql_script1 = file.read()
            print(f"\sql_script:\n  {sql_script1} \n")
            input("Presione enter para continuar")
            cursor.execute(sql_script1) 
            logger.info("Tabla 'registros_modbus' creada con éxito")
        #with open('database/registros_modbus_2.sql', 'r') as file:
        #    print("Insertando registros en tabla registros_modbus")
        #    sql_script2 = file.read()
        #    print(f"\sql_script:\n  {sql_script2} \n")
        #    input("Presione enter para continuar")
        #    cursor.execute(sql_script2) #fix
        #    logger.info("registros insertados en 'registros_modbus' con éxito")            


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