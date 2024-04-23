#src/main.py
from db_operations import check_db_connection, update_database
from controller import read_digital_input, inicializar_conexion_modbus, ModbusConnectionError, process_high_resolution_register, limpiar_pantalla
from logs.config_logger import configurar_logging
from DataTransfer import MainTransfer
import minimalmodbus
import time
import signal

# Configurar logging
logger = configurar_logging()

D1 = 70
D2 = 71
HR_COUNTER1_LO = 22
HR_COUNTER1_HI = 23
HR_COUNTER2_LO = 24
HR_COUNTER2_HI = 25


def main_loop():
    """
    Ejecuta el bucle principal del programa, procesando operaciones Modbus continuamente.

    Esta función define un bucle infinito que, en cada iteración, espera un segundo y luego
    ejecuta las operaciones relacionadas con Modbus. Está diseñada para mantener el programa
    en ejecución y procesando datos de manera continua.

    Proceso:
        - Entra en un bucle infinito.
        - En cada iteración, pausa la ejecución durante un segundo para evitar la sobrecarga.
        - Llama a la función `process_modbus_operations` para realizar las operaciones necesarias con el dispositivo Modbus.

    Nota:
        - Este bucle es infinito y el programa debe ser detenido manualmente o mediante señales del sistema.
        - La pausa de un segundo es importante para evitar el uso excesivo de recursos, especialmente en un contexto de comunicación con hardware.
    """
    global running
    running = True
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while running:
        logger.info("Ejecutando iteración del bucle principal.")
        MainTransfer()
        process_modbus_operations()
        time.sleep(1)
        limpiar_pantalla()


def handle_signal(signum, frame):
    global running
    running = False
    logger.info("Señal de terminación recibida. Terminando el bucle principal...")

def process_modbus_operations():
    """
    Gestiona las operaciones de comunicación Modbus y base de datos.

    Establece conexiones tanto con el dispositivo Modbus como con la base de datos.
    Si ambas conexiones son exitosas, procesa las entradas digitales y los registros
    de alta resolución del dispositivo Modbus y actualiza la base de datos en consecuencia.

    - Primero, intenta establecer una conexión con la base de datos.
    - Luego, intenta establecer una conexión con el dispositivo Modbus.
    - Si ambas conexiones son exitosas:
        * Procesa las entradas digitales del dispositivo Modbus.
        * Procesa los registros de alta resolución del dispositivo Modbus.
    - Si alguna conexión falla, el proceso se detiene y se manejan las excepciones correspondientes.
    """
    try:
        com_port, device_address = inicializar_conexion_modbus()
    except ModbusConnectionError as e:
        logger.error(f"Error de conexión Modbus: {e}")
        return

    try:
        connection = establish_db_connection()
    except DatabaseConnectionError as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        return

    instrument = establish_modbus_connection(com_port, device_address)
   
    process_digital_input(instrument, connection)
    process_high_resolution_register(instrument, connection)

def establish_db_connection():
    """
    Establece una conexión con la base de datos utilizando una función auxiliar.

    Esta función utiliza `establish_connection`, una función de alto nivel, para intentar
    establecer una conexión con la base de datos. Si la conexión falla, se maneja 
    la excepción correspondiente.

    Returns:
        Una conexión activa a la base de datos si es exitosa; de lo contrario, levanta una excepción.

    Proceso:
        - Intenta establecer una conexión con la base de datos utilizando `check_db_connection`.
        - Si falla la conexión, se levanta `DatabaseConnectionError` con un mensaje de error.
    """
    return establish_connection(
        check_db_connection, 
        "Error de conexión a la base de datos", 
        DatabaseConnectionError
    )

def establish_modbus_connection(com_port, device_address):
    """
    Establece una conexión con un dispositivo Modbus utilizando un puerto serie específico.

    Utiliza la función `establish_connection` para crear y configurar una instancia de 
    `minimalmodbus.Instrument`. Esta instancia se utiliza para interactuar con un dispositivo 
    Modbus a través de un puerto serie. En caso de error al configurar la conexión, se levanta
    una excepción `ModbusConnectionError`.

    Returns:
        Una instancia de `minimalmodbus.Instrument` configurada para comunicarse con el 
        dispositivo Modbus si la conexión es exitosa; de lo contrario, levanta una excepción.

    Proceso:
        - Intenta crear y configurar una instancia de `minimalmodbus.Instrument` usando el puerto
          serie especificado en `com_port` y la dirección del dispositivo en `device_address`.
        - Si falla la configuración del puerto serie, se levanta `ModbusConnectionError` con un
          mensaje de error.
    """
    return establish_connection(
        lambda: minimalmodbus.Instrument(com_port, device_address), 
        "Error al configurar el puerto serie", 
        ModbusConnectionError
    )

def establish_connection(connect_func, error_message, error_exception):
    """
    Intenta establecer una conexión o realizar una operación y maneja las excepciones.

    Esta función general se utiliza para intentar realizar cualquier operación que pueda lanzar
    una excepción. Captura excepciones genéricas y, en caso de error, imprime un mensaje de error
    personalizado y lanza una excepción específica.

    Args:
        connect_func (function): Función sin argumentos que intenta establecer una conexión o realizar una operación.
        error_message (str): Mensaje de error personalizado para mostrar si la operación falla.
        error_exception (Exception): Tipo de excepción a lanzar si la operación falla.

    Returns:
        El resultado de la función `connect_func` si la operación es exitosa.

    Raises:
        error_exception: Una excepción específica con un mensaje detallado si `connect_func` falla.

    Proceso:
        - Intenta ejecutar `connect_func`.
        - Si se produce una excepción, imprime `error_message` con detalles del error y lanza `error_exception`.
    """
    try:
        return connect_func()
    except Exception as e:
        logger.error(f"{error_message}: {e}")
        raise error_exception(f"{error_message}. Detalles: {e}") from e

def process_digital_input(instrument, connection):
    """
    Procesa las entradas digitales de un dispositivo Modbus y actualiza la base de datos.

    Lee el estado de las entradas digitales del dispositivo Modbus especificado y actualiza
    la base de datos con estos valores. Se realizan lecturas para múltiples entradas digitales
    y se actualizan sus estados correspondientes en la base de datos.

    Args:
        instrument (minimalmodbus.Instrument): El instrumento Modbus utilizado para la lectura.
        connection (pymysql.connections.Connection): La conexión a la base de datos para la actualización.

    Procedimiento:
        - Lee el estado de la entrada digital 1 (D1) y actualiza su estado en la base de datos con la etiqueta "HR_INPUT1_STATE".
        - Repite el proceso para la entrada digital 2 (D2) con la etiqueta "HR_INPUT2_STATE".
    """
    process_input_and_update(instrument, connection, read_digital_input, D1, "HR_INPUT1_STATE")
    process_input_and_update(instrument, connection, read_digital_input, D2, "HR_INPUT2_STATE")
    
def process_input_and_update(instrument, connection, read_function, address, description):
    """
    Lee un valor de un dispositivo Modbus y actualiza la base de datos.

    Utiliza una función de lectura específica para obtener el estado o valor de una dirección
    específica en un dispositivo Modbus. Si se obtiene un valor válido (no None), actualiza
    la base de datos con este valor.

    Args:
        instrument (minimalmodbus.Instrument): El instrumento Modbus utilizado para la lectura.
        connection (pymysql.connections.Connection): Conexión a la base de datos para actualizar el valor.
        read_function (function): Función específica de lectura de Modbus que se utilizará.
        address (int): Dirección en el dispositivo Modbus desde la que leer.
        description (str): Descripción del valor leído, utilizada para la actualización en la base de datos.

    Proceso:
        - Utiliza la función de lectura para obtener el valor de la dirección específica del dispositivo Modbus.
        - Si se obtiene un valor (distinto de None), actualiza la base de datos con este valor y la descripción proporcionada.
    """
    try:
        state = read_function(instrument, address)
        if state is not None:
            update_database(connection, address, state, descripcion=description)
    except minimalmodbus.ModbusException as e:
        raise ModbusReadError(f"Error al leer la dirección {address} del dispositivo Modbus: {e}") from e



class DatabaseConnectionError(Exception):
    """Excepción para errores de conexión con la base de datos."""
    pass

class ModbusReadError(Exception):
    """Excepción para errores de lectura del dispositivo Modbus."""
    pass

main_loop()
