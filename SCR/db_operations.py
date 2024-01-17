# db_operations.py
import pymysql
from logs.config_logger import configurar_logging
import functools
import os

logger = configurar_logging()

def update_database(connection, address, value, descripcion):
    """
    Actualiza un registro en la base de datos con un valor específico.

    Esta función construye y ejecuta una consulta SQL para actualizar un registro en la base de datos.
    Imprime un mensaje indicando si la actualización fue exitosa o no. En caso de errores en la ejecución
    de la consulta, lanza una excepción personalizada `DatabaseUpdateError`.

    Args:
        connection (pymysql.connections.Connection): La conexión activa a la base de datos.
        address (int): La dirección del registro en la base de datos a actualizar.
        value: El valor a asignar en el registro especificado.
        descripcion (str): Descripción del registro para mostrar en mensajes de log.

    Raises:
        DatabaseUpdateError: Si ocurre un error al actualizar la base de datos.

    Returns:
        None
    """
    try:
        query, params = build_update_query(address, value)
        if execute_query(connection, query, params):
            logger.info(f"Registro actualizado: dirección {address}, {descripcion} valor {value}")
        else:
            logger.error(f"No se pudo actualizar el registro: dirección {address}, {descripcion}")
    except pymysql.MySQLError as e:
        raise DatabaseUpdateError(f"Error al actualizar la base de datos en la dirección {address} con el valor {value}: {e}") from e

def build_update_query(address, value):
    """
    Construye una consulta SQL de actualización y sus parámetros.

    Esta función genera una consulta SQL para actualizar un registro en la tabla 'registros_modbus',
    utilizando la dirección del registro y el nuevo valor a asignar. La consulta se construye de
    manera parametrizada para prevenir inyecciones SQL.

    Args:
        address (int): La dirección del registro en la base de datos a actualizar.
        value: El nuevo valor a asignar en el registro especificado.

    Returns:
        tuple: Una tupla conteniendo la consulta SQL como string y los parámetros como una tupla.
    """
    query = "UPDATE registros_modbus SET valor = %s WHERE direccion_modbus = %s"
    params = (value, address)
    return query, params

def execute_query(connection, query, params):
    """
    Ejecuta una consulta SQL en la base de datos especificada.

    Esta función intenta ejecutar una consulta SQL utilizando la conexión y los parámetros proporcionados.
    En caso de éxito, confirma (commit) la transacción. Si ocurre un error durante la ejecución de la consulta,
    imprime un mensaje de error y retorna False.

    Args:
        connection (pymysql.connections.Connection): La conexión activa a la base de datos.
        query (str): La consulta SQL a ejecutar.
        params (tuple): Parámetros para la consulta SQL.

    Returns:
        bool: True si la consulta se ejecuta con éxito, False en caso de error.
    """
    if not connection:
        logger.error("No hay una conexión activa a la base de datos.")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
        return True
    except Exception as e:
        logger.error(f"Error al ejecutar la consulta en la base de datos: {e}")
        return False

def reconnect_on_failure(func):
    """
    Decorador que intenta reconectar a la base de datos en caso de un fallo en la conexión.

    Este decorador envuelve una función que realiza operaciones de base de datos. Si se detecta
    un error de conexión operacional o de MySQL durante la ejecución de la función, intenta
    establecer una nueva conexión y reintentar la operación.

    Args:
        func (function): La función que se va a decorar.

    Returns:
        function: La función envuelta con lógica de manejo de errores y reconexión.
    """
    @functools.wraps(func)
    def wrapper_reconnect(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (pymysql.OperationalError, pymysql.MySQLError) as e:
            print(f"Se detectó un error en la conexión a la base de datos: {e}. Intentando reconectar...")
            try:
                db_config = get_db_config()  # Obtener la configuración actualizada de la base de datos
                connection = pymysql.connect(**db_config)
                args = (connection,) + args[1:]
                return func(*args, **kwargs)
            except Exception as e:
                print(f"No se pudo reconectar a la base de datos: {e}")
                return None
    return wrapper_reconnect

@reconnect_on_failure
def check_db_connection():
    """
    Establece una conexión a la base de datos utilizando la configuración definida.

    Esta función intenta conectarse a la base de datos utilizando los parámetros especificados
    en la configuración de la base de datos. Está decorada con 'reconnect_on_failure', lo que
    asegura que intentará reconectar automáticamente en caso de fallar la conexión inicial.

    Returns:
        pymysql.connections.Connection: Un objeto de conexión a la base de datos.
    """
    db_config = get_db_config()  # Obtener la configuración de la base de datos
    connection = pymysql.connect(**db_config)
    return connection

class DatabaseUpdateError(Exception):
    """Excepción para errores en la actualización de la base de datos."""
    pass

def get_db_config():
    """
    Obtiene la configuración de la base de datos desde variables de entorno.

    Esta función construye un diccionario con la configuración necesaria para conectarse a una base de datos MySQL.
    Los valores de configuración se obtienen de variables de entorno, proporcionando una forma segura y flexible
    de manejar la configuración sin hardcodear valores en el código.

    Los valores por defecto son proporcionados para cada parámetro, que se usarán si las variables de entorno
    correspondientes no están definidas.

    Returns:
        dict: Un diccionario que contiene los parámetros de configuración de la base de datos, incluyendo
              host, usuario, contraseña, nombre de la base de datos y puerto.
    """
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', '12345678'),
        'db': 'novus',
        'port': 3306  
    }
