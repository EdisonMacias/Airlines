from app import app
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()  # Toma las variables de entorno de .env

# Configuración de la conexión MySQL

app.config['MYSQL_USER'] = 'b3fa59e401344c'
app.config['MYSQL_PASSWORD'] = '93cffd16'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'
app.config['MYSQL_DB'] = 'heroku_3544c227dec389d'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Crear la instancia de MySQL
mysql = MySQL(app)


