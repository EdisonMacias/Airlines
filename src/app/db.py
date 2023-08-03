from app import app
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()  # Toma las variables de entorno de .env

# Configuración de la conexión MySQL
mysql = MySQL(app)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Obtén la URL de conexión de la base de datos de la variable de entorno DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Remove 'mysql://' from the beginning of the URL
    db_info = database_url.replace('mysql://', '')

    # Extract user and password
    user_pass, host_db = db_info.split('@')
    user, password = user_pass.split(':')

    # Extract host and database name
    host, database = host_db.split('/')

    # Update app configuration
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_DB'] = database



