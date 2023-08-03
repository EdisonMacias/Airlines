from app import app
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()  # Toma las variables de entorno de .env

# Configuración de la conexión MySQL



database_url = os.environ.get('DATABASE_URL')
if database_url:
    url_parts = urlparse(database_url)
    app.config['MYSQL_USER'] = url_parts.username
    app.config['MYSQL_PASSWORD'] = url_parts.password
    app.config['MYSQL_HOST'] = url_parts.hostname
    app.config['MYSQL_DB'] = url_parts.path.lstrip('/')

mysql = MySQL(app)


