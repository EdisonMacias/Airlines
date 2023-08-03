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
    mysql_info = database_url.split('//')[0].split(':')
    app.config['MYSQL_USER'] = mysql_info[0]
    app.config['MYSQL_PASSWORD'] = mysql_info[0].split('@')[0]
    app.config['MYSQL_HOST'] = mysql_info[0].split('@')[0].split('/')[0]
    app.config['MYSQL_DB'] = mysql_info[0].split('@')[0].split('/')[0].split('?')[0]


