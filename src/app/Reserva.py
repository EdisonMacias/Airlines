from flask import Blueprint, request, render_template, redirect, url_for, flash
from db import mysql
from login import login_required

reserva = Blueprint('reserva', __name__, template_folder='app/templates')

@reserva.route('/reserva')
@login_required
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservaciones')
    data = cur.fetchall()
    cur.execute('SELECT * FROM destinos')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM clientes')
    data2 = cur.fetchall()
    cur.execute('SELECT r.id, c.nombre as cliente, d.nombre as destino, r.fecha_reservacion FROM reservaciones r JOIN clientes c ON r.cliente_id = c.id JOIN destinos d ON r.destino_id = d.id')
    data3 = cur.fetchall()
    cur.close()
    return render_template('Reserva.html', reservar=data3, reserva=data, destino=data1, cliente=data2)

@reserva.route('/add_reserva', methods=['POST'])
@login_required
def add_reserva():
    if request.method == 'POST':
        destino = request.form['destino']
        cliente = request.form['cliente']
        reser = request.form['reser']
        try:
            cur = mysql.connection.cursor()
            cur.execute("Select id from destinos where nombre = %s",(destino,))
            dest = cur.fetchone()
            cur.execute("Select id from clientes where nombre = %s",(cliente,))
            clt = cur.fetchone()
            cur.execute(
                "INSERT INTO reservaciones (destino_id, cliente_id, fecha_reservacion) VALUES (%s,%s,%s)", (dest["id"],clt["id"],reser))
            mysql.connection.commit()
            flash('Reservacion Agregado correctamente')
            return redirect(url_for('reserva.Index'))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('reserva.Index'))

@reserva.route('/editReserva/<id>', methods=['POST', 'GET'])
@login_required
def get_reserva(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservaciones WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.execute('SELECT * FROM destinos')
    data1 = cur.fetchall()
    cur.execute('SELECT * FROM clientes')
    data2 = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-reserva.html', reserva=data[0], destino=data1, cliente=data2)

@reserva.route('/updateReserva/<int:id>', methods=['POST'])
@login_required
def update_reserva(id):
    if request.method == 'POST':
        destino = request.form['destino']
        cliente = request.form['cliente']
        reser = request.form['reser']
        cur = mysql.connection.cursor()
        cur.execute("Select id from destinos where nombre = %s",(destino,))
        dest = cur.fetchone()
        cur.execute("Select id from clientes where nombre = %s",(cliente,))
        clt = cur.fetchone()
        cur.execute("""
            UPDATE reservaciones
            SET destino_id = %s,
                cliente_id = %s,
                fecha_reservacion = %s
            WHERE id = %s
        """, (dest["id"], clt["id"], reser, id))
        flash('Reservacion actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('reserva.Index'))

@reserva.route('/deleteReserva/<string:id>', methods=['POST', 'GET'])
@login_required
def delete_reserva(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM reservaciones WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Reservacion eliminado correctamente')
    return redirect(url_for('reserva.Index'))
