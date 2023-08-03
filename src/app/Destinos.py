from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql
from login import login_required

destino = Blueprint('destino', __name__, template_folder='app/templates')


@destino.route('/destino')
@login_required
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Destinos')
    data = cur.fetchall()
    
    cur.close()
    return render_template('Destinos.html', destino=data)

@destino.route('/add_destino', methods=['POST'])
@login_required
def add_destino():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        inicio = request.form['inicio']
        fin = request.form['fin']
        descrip = request.form['descripcion']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO destinos (nombre, ubicacion, fechaInicio, fechaFin, Descripcion) VALUES (%s,%s,%s,%s,%s)", (nombre, ubicacion, inicio, fin, descrip))
            mysql.connection.commit()
            flash('Destino Agregado correctamente')
            return redirect(url_for('destino.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('destino.Index'))


@destino.route('/editDestino/<int:id>', methods=['POST', 'GET'])
@login_required
def get_destino(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM destinos WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-destino.html', destino=data[0])


@destino.route('/updateDestino/<id>', methods=['POST'])
@login_required
def update_destino(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        ubicacion = request.form['ubicacion']
        inicio = request.form['inicio']
        fin = request.form['fin']
        descrip = request.form['descripcion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE destinos
            SET nombre = %s,
                ubicacion = %s,
                fechaInicio = %s,
                fechaFin = %s,
                descripcion = %s
            WHERE id = %s
        """, (nombre, ubicacion, inicio, fin, descrip, id))
        flash('Destino actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('destino.Index'))


@destino.route('/deleteDestino/<string:id>', methods=['POST', 'GET'])
@login_required
def delete_destino(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservaciones WHERE destino_id = %s',(id,))
    data =cur.fetchall()
    if data:
        cur.close()
        flash('No se puede eliminar destino, el destino tiene una reservacion')
        return redirect(url_for('destino.Index'))
    else:
        cur.execute('DELETE FROM destinos WHERE id = {0}'.format(id))
        mysql.connection.commit()
        flash('Destino eliminado correctamente')
        return redirect(url_for('destino.Index'))
