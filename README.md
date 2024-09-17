
# Proyecto Automatización AGROBAC

Este proyecto consiste en un script de Python que automatiza la ejecución de consultas SQL, maneja transacciones y genera un log detallado de la ejecución.

## Requisitos

- **Python 3.8 o superior** (instalación desde el sitio oficial).
- **Biblioteca pyodbc** para la conexión a bases de datos SQL Server.
- **Entorno virtual** para gestionar las dependencias del proyecto.

## Instalación de Python

1. Dirígete al sitio oficial de Python: [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Descarga la versión más reciente de Python compatible con tu sistema operativo (asegúrate de descargar Python 3.8 o superior).
3. Sigue los pasos del instalador. **Asegúrate de marcar la opción "Add Python to PATH"** durante la instalación para que Python pueda ser ejecutado desde la línea de comandos.
4. Verifica la instalación abriendo una terminal (CMD, PowerShell o Bash) y ejecutando el siguiente comando:

   ```bash
   python --version
   ```

   Debería mostrar la versión de Python instalada.

## Creación del entorno virtual

1. Navega a la carpeta raíz del proyecto donde se encuentra el script en tu terminal.
2. Crea un entorno virtual llamado `agrobac` ejecutando el siguiente comando:

   ```bash
   python -m venv agrobac
   ```

   Esto creará una carpeta llamada `agrobac` en tu proyecto, que contendrá el entorno virtual con las dependencias aisladas del sistema.

## Activación del entorno virtual

Dependiendo del sistema operativo que utilices, deberás ejecutar uno de los siguientes comandos para activar el entorno virtual:

- **Windows**:

  ```bash
  agrobac\Scripts\activate
  ```

- **Linux/MacOS**:

  ```bash
  source agrobac/bin/activate
  ```

Una vez activado el entorno, deberías ver `(agrobac)` al inicio de tu línea de comandos, lo que indica que estás utilizando el entorno virtual.

## Instalación de la biblioteca pyodbc

Con el entorno virtual activado, instala la biblioteca `pyodbc`, que es necesaria para la conexión a la base de datos SQL Server. Ejecuta el siguiente comando:

```bash
pip install pyodbc
```

Esto descargará e instalará la biblioteca necesaria en el entorno virtual.

## Ejecución del script

Una vez que el entorno virtual esté activado y la biblioteca `pyodbc` instalada, puedes ejecutar el script principal de la siguiente manera:

```bash
python main.py
```

El script comenzará a ejecutarse, procesando las líneas SQL y generando un log de las operaciones realizadas.

## Desactivación del entorno virtual

Cuando termines de trabajar en el proyecto, puedes desactivar el entorno virtual ejecutando:

```bash
deactivate
```

## Notas

- Asegúrate de que las credenciales de la base de datos y los detalles de conexión estén correctamente configurados en el script `main.py`.
- No olvides agregar tu entorno virtual al archivo `.gitignore` para evitar que sea rastreado por Git:

  ```bash
  agrobac/
  ```

---

¡Eso es todo! Este archivo `README.md` te guía a través de los pasos necesarios para instalar Python, configurar el entorno virtual, y ejecutar el script en este proyecto.
