#SCR/DataTranfer.py
import time
from datetime import datetime
from logs.config_logger import configurar_logging
from db_operations import check_db_connection  
import pymysql
import subprocess


logger = configurar_logging()

def MainTransfer():
    """
    Función para verificar y ejecutar la transferencia de datos.
    """
    try:
        print("")
        if es_tiempo_cercano_multiplo_cinco():
            logger.info("Iniciando la transferencia de datos.")
            consulta1 = """
            SELECT 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_LO') AS HR_COUNTER1_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER1_HI') AS HR_COUNTER1_HI, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_LO') AS HR_COUNTER2_LO, 
                (SELECT valor FROM registros_modbus WHERE registro = 'HR_COUNTER2_HI') AS HR_COUNTER2_HI;
            """
            consulta2 = """
            INSERT INTO ProductionLog (unixtime, HR_COUNTER1_LO, HR_COUNTER1_HI, HR_COUNTER2_LO, HR_COUNTER2_HI)
            VALUES (%s, %s, %s, %s, %s)
            """
            num_filas = 5
            transferir_datos(consulta1,consulta2,num_filas)
            consulta1 = """
            SELECT 
                ((SELECT HR_COUNTER1_LO FROM ProductionLog ORDER BY ID DESC LIMIT 1) - 
                (SELECT HR_COUNTER1_LO FROM ProductionLog WHERE ID = (SELECT MAX(ID) - 1 FROM ProductionLog))) AS HR_COUNTER1,
                ((SELECT HR_COUNTER2_LO FROM ProductionLog ORDER BY ID DESC LIMIT 1) - 
                (SELECT HR_COUNTER2_LO FROM ProductionLog WHERE ID = (SELECT MAX(ID) - 1 FROM ProductionLog))) AS HR_COUNTER2
            FROM ProductionLog
            LIMIT 1;
            """
            consulta2 = """
            INSERT INTO intervalproduction (unixtime, HR_COUNTER1, HR_COUNTER2)
            VALUES (%s, %s, %s)
            """
            num_filas = 3
            transferir_datos(consulta1,consulta2,num_filas)
            SendDataPHP()

            time.sleep(1)

        else:
            logger.info("No es momento de transferir datos. Esperando para la próxima verificación.")
    except Exception as e:
        logger.error(f"Error en MainTransfer: {e}")

def SendDataPHP():
    # Define la ruta al intérprete de PHP y al script PHP utilizando raw strings
    php_interpreter = "C://AppServ//php7//php.exe"
    php_script = "C://AppServ//www//DataMaq//includes//SendData_python.php"

    # Ejecuta el script PHP usando subprocess.run
    result = subprocess.run([php_interpreter, php_script], capture_output=True, text=True, shell=True)

    # Log y manejo del resultado
    if result.returncode == 0:
        logger.info("Script PHP ejecutado exitosamente. Salida:")
        logger.info(result.stdout)
    else:
        logger.error(f"Error al ejecutar el script PHP. Código de salida: {result.returncode}")
        logger.error(result.stderr)


def transferir_datos(consulta1, consulta2, num_filas):
    """
    Función principal para transferir datos.
    """
    print("")
    try:
        conn = check_db_connection()
        if not conn:
            logger.error("No se pudo establecer una conexión con la base de datos.")
            return
        with conn.cursor() as cursor:
            logger.info("Iniciando la transferencia de datos.")
            unixtime = int(time.time())
            unixtime = (round(unixtime/300))*300
            datos_originales = obtener_datos(cursor, consulta1)
            # Convertir los elementos de cada tupla de cadena a entero
            datos = [(unixtime,) + tuple(int(x) for x in fila) for fila in datos_originales]
            if datos:
                # Verificar si ya existe un registro con el mismo unixtime
                cursor.execute("SELECT COUNT(*) FROM intervalproduction WHERE unixtime = %s", (unixtime,))
                if cursor.fetchone()[0] == 0:
                    # Solo insertar si no hay registros existentes con el mismo unixtime
                    insertar_datos(conn, datos, consulta2, num_filas)
                    conn.commit()
                    logger.info("Transferencia de datos completada exitosamente.")
                else:
                    logger.warning("Se evitó la inserción de un registro duplicado para el unixtime %s.", unixtime)
            else:
                logger.warning("No se obtuvieron datos para transferir.")
    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL durante la transferencia de datos: {e}")
        conn.rollback()
    except Exception as e:
        logger.error(f"Error inesperado durante la transferencia de datos: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            logger.info("Conexión a la base de datos cerrada.")


def obtener_datos(cursor, consulta):
    """
    Ejecuta una consulta SQL y devuelve los resultados.

    Args:
        cursor: Cursor de la base de datos.
        consulta (str): Consulta SQL a ejecutar.

    Returns:
        list: Resultados de la consulta o None en caso de error.
    """
    try:
        cursor.execute(consulta)
        return cursor.fetchall()
    except pymysql.MySQLError as e:
        logger.error(f"Error de MySQL al ejecutar consulta: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al ejecutar consulta: {e}")
    return None

def insertar_datos(conn, datos, consulta2,num_filas):
    """
    Inserta los datos obtenidos.

    Args:
        conn: Conexión a la base de datos.
        datos: Datos a insertar.
        consulta2 (str): Consulta SQL para la inserción de datos.
    """
    try:
        with conn.cursor() as cursor:
            for fila in datos:
                # Asegurarse de que 'fila' tiene exactamente tres elementos
                # Por ejemplo: fila = (unixtime, HR_COUNTER1, HR_COUNTER2)
                if len(fila) == num_filas:
                    cursor.execute(consulta2, fila)
                else:
                    logger.warning("Fila con número incorrecto de elementos: %s", fila)
            conn.commit()
            logger.info("%s registros insertados con éxito.", len(datos))
    except pymysql.MySQLError as e:
        logger.error("Error de MySQL al insertar datos: %s", e)
        conn.rollback()
    except Exception as e:
        logger.error("Error inesperado al insertar datos: %s", e)
        conn.rollback()

def es_tiempo_cercano_multiplo_cinco(tolerancia=5):
    """
    Verifica si el tiempo actual está cerca de un múltiplo de 5 minutos.

    Args:
        tolerancia (int): Número de segundos de tolerancia para considerar 'cercano'.

    Returns:
        bool: True si el tiempo actual está dentro de la tolerancia de un múltiplo de 5 minutos, False de lo contrario.
    """
    ahora = datetime.now()
    minuto_actual = ahora.minute
    segundo_actual = ahora.second

    cercano_a_multiplo = minuto_actual % 5 <= tolerancia / 60 and segundo_actual <= tolerancia
    logger.info(f"Chequeando tiempo: {ahora}, cercano a múltiplo de 5: {'sí' if cercano_a_multiplo else 'no'}")
    return cercano_a_multiplo


def sincronizar_intervalproduction():
    """
    Sincroniza la tabla 'intervalproduction' entre las bases de datos local y remota.
    """
    try:
        logger.info("Iniciando la sincronización de 'intervalproduction'.")
        
        # Establecer conexión con la base de datos local
        conn_local = check_db_connection(remote=False)
        logger.info("Conexión establecida con la base de datos local.")

        # Establecer conexión con la base de datos remota
        conn_remota = check_db_connection(remote=True)
        logger.info("Conexión establecida con la base de datos remota.")

        with conn_local.cursor() as cursor_local, conn_remota.cursor() as cursor_remoto:
            logger.info("Cursore para ambas bases de datos creados.")

            # Obtener los últimos registros de ambas bases de datos
            logger.info("Obteniendo el último registro de la base de datos local.")
            ultimo_registro_local = obtener_ultimo_registro(cursor_local)
            logger.info(f"Último registro local: {ultimo_registro_local}")

            logger.info("Obteniendo el último registro de la base de datos remota.")
            ultimo_registro_remoto = obtener_ultimo_registro(cursor_remoto)
            logger.info(f"Último registro remoto: {ultimo_registro_remoto}")

            # Comparar y sincronizar
            if ultimo_registro_local != ultimo_registro_remoto:
                logger.info("Las bases de datos no están sincronizadas. Iniciando sincronización.")
                # Código para sincronizar los registros...
                pass
            else:
                logger.info("Las bases de datos ya están sincronizadas.")

    except Exception as e:
        logger.error(f"Error en la sincronización de las bases de datos: {e}")

def obtener_ultimo_registro(cursor):
    """
    Obtiene el último registro de la tabla 'intervalproduction'.

    Args:
        cursor: Cursor de la base de datos.

    Returns:
        tuple: El último registro de la tabla.
    """
    try:
        consulta = "SELECT * FROM intervalproduction ORDER BY ID DESC LIMIT 1"
        cursor.execute(consulta)
        registro = cursor.fetchone()
        logger.info(f"Consulta ejecutada exitosamente. Registro obtenido: {registro}")
        return registro
    except Exception as e:
        logger.error(f"Error al obtener el último registro: {e}")
        raise
