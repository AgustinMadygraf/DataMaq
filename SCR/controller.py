#SCR/controller.py
from logs.config_logger import configurar_logging
from db_operations import update_database
import serial.tools.list_ports

D1 = 70
D2 = 71
HR_COUNTER1_LO = 22
HR_COUNTER1_HI = 23

logger = configurar_logging()

def read_digital_input(instrument, address):
    """
    Lee el estado de una entrada digital de un dispositivo Modbus.

    Utiliza la función 'safe_modbus_read' para realizar una lectura segura de un bit del dispositivo
    Modbus especificado. Esta función se enfoca en leer estados de entradas digitales, como sensores on/off.

    Args:
        instrument (minimalmodbus.Instrument): El instrumento Modbus utilizado para la lectura.
        address (int): La dirección de la entrada digital a leer en el dispositivo Modbus.

    Returns:
        int/None: El estado de la entrada digital (1 o 0) si la lectura es exitosa, o None si ocurre un error.
    """
    return safe_modbus_read(instrument.read_bit, address, functioncode=2)

def inicializar_conexion_modbus():
    """
    Inicializa la conexión con el dispositivo Modbus, detectando el puerto serie adecuado.

    Esta función busca un puerto serie disponible que coincida con las descripciones de los dispositivos
    'DigiRail Connect' o 'USB-SERIAL CH340'. Si se encuentra un puerto correspondiente, se retorna su nombre
    junto con la dirección predefinida del dispositivo Modbus.

    Returns:
        tuple: Una tupla que contiene el nombre del puerto serie encontrado y la dirección del dispositivo Modbus.

    Raises:
        SystemExit: Si no se detecta ningún puerto COM para el dispositivo.

    Proceso:
        - Intenta detectar un puerto serie para 'DigiRail Connect'.
        - Si no se encuentra, intenta detectar 'USB-SERIAL CH340'.
        - Si se encuentra un puerto, retorna su nombre y la dirección del dispositivo Modbus.
        - Si no se detecta ningún puerto, muestra un mensaje de error y sale del programa.
    """
    device_address = 1
    device_description = "DigiRail Connect"  
    com_port = detect_serial_ports(device_description)
    print("")
    if com_port:
        logger.info(f"Puerto {device_description} detectado: {com_port}")
    else:
        device_description = "USB-SERIAL CH340"  
        com_port = detect_serial_ports(device_description)
        if com_port:
            logger.info(f"Puerto detectado: {com_port}\n")
        else:
            logger.error("No se detectaron puertos COM para tudispositivo.")
            input("Presiona una tecla para salir")
            exit()
    return com_port, device_address

def process_high_resolution_register(instrument, connection):
    """
    Procesa y actualiza los registros de alta resolución de un dispositivo Modbus.

    Lee los valores de los registros HR_COUNTER1_LO y HR_COUNTER1_HI del dispositivo Modbus
    y actualiza la base de datos con estos valores individualmente.

    Args:
        instrument (minimalmodbus.Instrument): El instrumento Modbus utilizado para la lectura.
        connection (pymysql.connections.Connection): Conexión a la base de datos para actualizar los valores.
    """
    value_lo = safe_modbus_read(instrument.read_register, HR_COUNTER1_LO, functioncode=3)
    if value_lo is not None:
        update_database(connection, HR_COUNTER1_LO, value_lo, "HR_COUNTER1_LO")

    value_hi = safe_modbus_read(instrument.read_register, HR_COUNTER1_HI, functioncode=3)
    if value_hi is not None:
        update_database(connection, HR_COUNTER1_HI, value_hi, "HR_COUNTER1_HI")

def detect_serial_ports(device_description):
    """
    Busca y retorna el nombre del puerto serie que coincide con la descripción del dispositivo dada.

    Esta función recorre todos los puertos serie disponibles en el sistema y compara la descripción
    de cada uno con la descripción del dispositivo proporcionada. Si encuentra una coincidencia,
    retorna el nombre del puerto serie correspondiente.

    Args:
        device_description (str): La descripción del dispositivo Modbus a buscar entre los puertos serie.

    Returns:
        str/None: El nombre del puerto serie que coincide con la descripción del dispositivo, o None si no se encuentra.
    """
    available_ports = list(serial.tools.list_ports.comports())
    for port, desc, hwid in available_ports:
        if device_description in desc:
            return port
    return None

def safe_modbus_read(method, *args, **kwargs):
    """
    Realiza una lectura segura de un dispositivo Modbus.

    Envuelve la llamada a un método de lectura Modbus en un bloque try-except para manejar excepciones.
    Proporciona un mecanismo de recuperación y registro de errores en caso de fallas en la lectura.

    Args:
        method (callable): Método de lectura Modbus a ser invocado.
        *args: Argumentos posicionales para el método de lectura.
        **kwargs: Argumentos de palabra clave para el método de lectura.

    Returns:
        El resultado del método de lectura si es exitoso, o None si ocurre una excepción.
    """
    try:
        return method(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error al leer del dispositivo Modbus: {e}")
        return None

class ModbusConnectionError(Exception):
    """Excepción para errores de conexión con el dispositivo Modbus."""
    pass
