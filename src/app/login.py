from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import mysql
from passlib.hash import bcrypt
import jwt
import datetime
from flask import current_app
from functools import wraps

login = Blueprint('login', __name__, template_folder='app/templates')

def login_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        # Aquí implementa la lógica para verificar si el usuario está autenticado
        # y si tiene los permisos adecuados para acceder a la página
        if not is_user_authenticated():
            flash('Debe iniciar sesión para acceder a esta página')
            return redirect('/')  # Reemplaza 'login' por el nombre de la ruta a la página de inicio de sesión

        # Si el usuario está autenticado y tiene los permisos adecuados, muestra la página solicitada
        return view_func(*args, **kwargs)

    return decorated_function

def is_user_authenticated():
    return 'user_id' in session

def generate_jwt_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token válido por 1 día
    }
    secret_key = current_app.config['SECRET_KEY']  # Asegúrate de tener configurada tu clave secreta en Flask
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

@login.route('/', methods=['GET','POST'])
def Index():
    if request.method == 'POST':
        Usuario = request.form['usuario']
        Contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute('SELECT Password FROM Admin WHERE Usuario = %s', (Usuario,))
        data = cur.fetchone()
        cur.execute('SELECT password FROM clientes WHERE nombre = %s', (Usuario,))
        data1 = cur.fetchone()
        if data and verify_password(Contraseña, data["Password"]):
            cur.close()
            session['user_id'] = verify_password(Contraseña, data["Password"])
            token = generate_jwt_token(Usuario)
            return redirect('/cliente?token=' + token)
        elif data1 and verify_password(Contraseña, data1["password"]):
            cur.execute('SELECT id FROM clientes WHERE nombre = %s', (Usuario,))
            data2 = cur.fetchone()
            cur.close()
            session['user_id'] = data2["id"]
            token = generate_jwt_token(Usuario)
            return redirect('/user?token='+token)
        else:
            cur.close()
            flash('Usuario y/o contraseña incorrectos')
            return render_template('index.html')
    return render_template('index.html')

# Ruta para cerrar sesión
@login.route('/logout')
def logout():
    # Eliminar el usuario de la sesión si está presente
    session.pop('user_id', None)
    return redirect(url_for('login.Index'))

def verify_password(input_password, hashed_password):
    return bcrypt.verify(input_password, hashed_password)

def encrypt_password(password):
    hashed_password = bcrypt.hash(password)  # Generar el hash bcrypt
    return hashed_password

# Función para insertar un nuevo usuario en la base de datos
def insert_user(nombre, apellido, correo, telefono, password):
    # Encriptar la contraseña antes de almacenarla
    hashed_password = encrypt_password(password)

    # Código para insertar el usuario y la contraseña en la base de datos
    # (Reemplaza esta parte con tu lógica para insertar en tu base de datos)
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO clientes (nombre, apellido, correo, telefono, password) VALUES (%s,%s,%s,%s,%s)",
            (nombre, apellido, correo, telefono, hashed_password))  # Almacenar el hash en la base de datos
        mysql.connection.commit()
        flash('Registro exitoso')
        return True
    except Exception as e:
        flash(e.args[1])
        return False

@login.route('/registro', methods=['GET','POST'])
def registros():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = request.form['password']

        # Insertar el nuevo usuario en la base de datos, ahora con la contraseña encriptada
        if insert_user(nombre, apellido, correo, telefono, password):
            return redirect(url_for('login.Index'))  # Redireccionar a la página de inicio de sesión después del registro

    return render_template('Registrar.html')