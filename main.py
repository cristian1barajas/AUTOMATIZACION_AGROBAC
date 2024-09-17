import pyodbc
import time
import logging
import os
import sys

# Configuración de conexiones (ejemplo)
CONEXIONES = {
    'local': {
        'server': 'BARAJAS',
        'database': 'AGROBAC_DEV',  # Nombre de la base de datos local
        'trusted_connection': True  # Usa autenticación Windows
    },
    'desarrollo': {
        'server': '20.163.199.84,50840',  # IP con puerto para servidor de desarrollo
        'database': 'AGROBAC_DEV',  # Nombre de la base de datos en desarrollo
        'username': 'sa',
        'password': '#dbAgrario2024$',
        'trusted_connection': False  # Autenticación con usuario y contraseña
    }
}

# Configuración de logging (archivo de log junto a main.py, usando UTF-8)
log_file = os.path.join(os.path.dirname(__file__), 'insert_log.txt')

# Configurar logging para escribir en archivo con codificación UTF-8
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_file, encoding='utf-8')])  # Forzar codificación UTF-8

# Variables de conteo global
contador_exitosos = 0
contador_fk_errors = 0
contador_otros_errores = 0

# Función para obtener la cadena de conexión
def obtener_cadena_conexion(entorno):
    if CONEXIONES[entorno]['trusted_connection']:
        return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={CONEXIONES[entorno]['server']};DATABASE={CONEXIONES[entorno]['database']};Trusted_Connection=yes;"
    else:
        return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={CONEXIONES[entorno]['server']};DATABASE={CONEXIONES[entorno]['database']};UID={CONEXIONES[entorno]['username']};PWD={CONEXIONES[entorno]['password']};"

# Función para ejecutar una línea SQL con validación
def ejecutar_linea_sql(cursor, linea_sql):
    global contador_exitosos, contador_fk_errors, contador_otros_errores
    try:
        # Verificar si la línea contiene un INSERT en la tabla [Dom].[Cuenta] con NumeroCuenta '903' o '1.2.10'
        if "INSERT INTO [Dom].[Cuenta]" in linea_sql and "VALUES" in linea_sql:
            if "'903'" in linea_sql or "'1.2.10'" in linea_sql:
                logging.info(f"Omitiendo el INSERT ya que NumeroCuenta '903' o '1.2.10' está siendo insertado.")
                return  # Omitir el INSERT

        # Ejecutar la línea SQL normalmente, pero sin imprimirla en consola
        cursor.execute(linea_sql)
        cursor.commit()  # Confirmar esta línea si se ejecuta correctamente
        contador_exitosos += 1  # Incrementar el contador de éxitos

    except pyodbc.IntegrityError as e:
        # Error por restricción de integridad (ej. Foreign Key)
        if "FOREIGN KEY" in str(e):
            logging.error(f"Error de llave foránea al ejecutar línea SQL: {linea_sql.strip()}")
            contador_fk_errors += 1
        else:
            logging.error(f"Error de integridad desconocido: {e}")
            contador_otros_errores += 1
    except pyodbc.Error as e:
        # Otros tipos de errores de SQL
        logging.error(f'Error al ejecutar línea SQL: {e}')
        logging.error(f"Línea SQL fallida: {linea_sql.strip()}")  # Registrar la línea fallida en log
        contador_otros_errores += 1

# Función para mostrar el porcentaje de avance y los contadores
def mostrar_progreso(actual, total):
    porcentaje = (actual / total) * 100
    # Actualiza los contadores en la misma línea en la consola
    sys.stdout.write(f"\rProgreso: {porcentaje:.2f}% | INSERTS Correctos: {contador_exitosos} | Errores FK: {contador_fk_errors} | Otros Errores: {contador_otros_errores}")
    sys.stdout.flush()  # Forzar la actualización de la línea en consola

# Manejo de interrupción
try:
    ENTORNO = 'local'  # Cambia según el entorno deseado (local o desarrollo)
    connection_string = obtener_cadena_conexion(ENTORNO)

    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()

        # Leer todas las líneas del archivo al inicio para saber el total
        with open('ADC_PROD_PARAM_1_20240830.sql', 'r', encoding='utf-8') as file:
            lineas = file.readlines()
        total_lineas = len(lineas)

        # Iniciar una transacción global
        conn.autocommit = False  # Deshabilitar autocommit para manejar la transacción manualmente

        # Procesar cada línea una por una e ignorar exclusivamente líneas que contengan solo 'GO'
        for lineas_leidas, linea in enumerate(lineas, start=1):
            mostrar_progreso(lineas_leidas, total_lineas)

            # Ignorar las líneas que solo contienen 'GO'
            if linea.strip().upper() == 'GO':
                logging.info(f"Ignorando línea 'GO': {linea.strip()}")
                continue

            # Ejecutar el resto de las líneas con validación para NumeroCuenta '903' y '1.2.10'
            if linea.strip():  # Evitar ejecutar líneas vacías
                ejecutar_linea_sql(cursor, linea)

        # Si todo sale bien, confirmar la transacción global
        conn.commit()
        logging.info("Todas las sentencias SQL han sido ejecutadas y confirmadas.")

except pyodbc.DatabaseError as db_err:
    # Si ocurre un error, revertir la transacción global
    logging.error("Se detuvo la ejecución debido a un error de base de datos.")
    logging.error(f"Detalles del error: {db_err}")
    conn.rollback()  # Revertir toda la transacción si hay un error
    logging.info("Se ha revertido toda la transacción debido al error.")

except KeyboardInterrupt:
    logging.warning("Ejecución interrumpida por el usuario.")
    conn.rollback()  # Revertir la transacción si el usuario interrumpe
    logging.info("Se ha revertido toda la transacción debido a la interrupción.")

finally:
    cursor.close()
    conn.close()

    # Mostrar el resumen final
    print("\n\n--- Resumen Final ---")
    print(f"INSERTS Correctos: {contador_exitosos}")
    print(f"Errores por llave foránea (FK): {contador_fk_errors}")
    print(f"Otros errores: {contador_otros_errores}")
