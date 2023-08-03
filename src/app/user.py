from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import mysql
from login import login_required

user = Blueprint('user', __name__, template_folder='app/templates')


@user.route('/user')
@login_required
def User():
    id = session.get('user_id')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM destinos')
    data = cur.fetchall()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    data1 = cur.fetchall()
    cur.close()
    return render_template('User.html', destino=data, cliente=data1[0])


@user.route('/add_reservar/<int:idd>/<int:idc>', methods=['POST'])
@login_required
def add_reservar(idd,idc):
    if request.method == 'POST':
        reser = request.form['reser']
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO reservaciones (destino_id, cliente_id, fecha_reservacion) VALUES (%s,%s,%s)", (idd ,idc ,reser))
            mysql.connection.commit()
            flash('Reservacion Agregado correctamente')
            return redirect(url_for('user.Info_Destino', idd=idd, idc=idc))
        except Exception as e:
            flash(e.args[1])
            return redirect(url_for('user.Info_Destino', idd=idd, idc=idc))

@user.route('/Info-destino/<int:idd>/<int:idc>')
@login_required
def Info_Destino(idd,idc):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', (idc,))
    data = cur.fetchall()
    cur.execute('SELECT * FROM destinos WHERE id = %s', (idd,))
    data1 = cur.fetchall()
    cur.close()
    return render_template('Info-destino.html', destino=data1[0], cliente=data[0])