from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import mysql
from login import login_required, encrypt_password
import re

cliente = Blueprint('cliente', __name__, template_folder='app/templates')

@cliente.route('/cliente')
@login_required
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Clientes')
    data = cur.fetchall()
    cur.close()
    return render_template('Cliente.html', cliente=data)


@cliente.route('/add_cliente', methods=['POST'])
@login_required
def add_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = request.form['password']
        # Validaciones
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$', nombre):
            flash('Ingresa un nombre válido.')
        elif not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$', apellido):
            flash('Ingresa un apellido válido.')
        elif not re.match(r'\S+@\S+\.\S+', correo):
            flash('Ingresa un correo electrónico válido.')
        elif not re.match(r'^\d{10}$', telefono):
            flash('Ingresa un número de teléfono válido (10 dígitos).')
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            flash('La contraseña debe tener al menos 8 caracteres y contener al menos una letra, un número y un carácter especial (@$!%*#?&).')
        else:
            try:
                session.pop('nombre', None)
                session.pop('apellido', None)
                session.pop('correo', None)
                session.pop('telefono', None)
                session.pop('password', None)
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO clientes (nombre, apellido, correo, telefono, password) VALUES (%s,%s,%s,%s,%s)", (nombre, apellido, correo, telefono, encrypt_password(password)))
                mysql.connection.commit()
                flash('Cliente Agregado correctamente')
                return redirect(url_for('cliente.Index'))
            except Exception as e:
                flash(e.args[1])

        # Almacenar los datos ingresados en la sesión flash
        session['nombre'] = nombre
        session['apellido'] = apellido
        session['correo'] = correo
        session['telefono'] = telefono
        session['password'] = password
        return redirect(url_for('cliente.Index'))


@cliente.route('/editCliente/<id>', methods=['POST', 'GET'])
@login_required
def get_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-cliente.html', cliente=data[0])


@cliente.route('/updateCliente/<id>', methods=['POST'])
@login_required
def update_cliente(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        password = request.form['password']
        # Validaciones
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$', nombre):
            flash('Ingresa un nombre válido.')
        elif not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$', apellido):
            flash('Ingresa un apellido válido.')
        elif not re.match(r'\S+@\S+\.\S+', correo):
            flash('Ingresa un correo electrónico válido.')
        elif not re.match(r'^\d{10}$', telefono):
            flash('Ingresa un número de teléfono válido (10 dígitos).')
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            flash('La contraseña debe tener al menos 8 caracteres y contener al menos una letra, un número y un carácter especial (@$!%*#?&).')
        else:
            session.pop('nombre', None)
            session.pop('apellido', None)
            session.pop('correo', None)
            session.pop('telefono', None)
            session.pop('password', None)
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE clientes
                SET nombre = %s,
                    apellido = %s,
                    correo = %s,
                    telefono = %s,
                    password = %s
                WHERE id = %s
            """, (nombre, apellido, correo, telefono, encrypt_password(password), id))
            flash('Cliente actualizado correctamente')
            mysql.connection.commit()
            return redirect(url_for('cliente.Index'))
    session['nombre'] = nombre
    session['apellido'] = apellido
    session['correo'] = correo
    session['telefono'] = telefono
    session['password'] = password
    return redirect(url_for('cliente.get_cliente',id=id))


@cliente.route('/deleteCliente/<string:id>', methods=['POST', 'GET'])
@login_required
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservaciones WHERE cliente_id = %s',(id,))
    data =cur.fetchall()
    if data:
        cur.close()
        flash('No se puede eliminar cliente, el cliente tiene una reservacion')
        return redirect(url_for('cliente.Index'))
    else:
        cur.execute('DELETE FROM clientes WHERE id = {0}'.format(id))
        mysql.connection.commit()
        flash('Cliente eliminado correctamente')
        return redirect(url_for('cliente.Index'))
