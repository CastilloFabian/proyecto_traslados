# app.py

import pymysql
pymysql.install_as_MySQLdb()

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = "centerbeam.proxy.rlwy.net"
app.config['MYSQL_PORT'] = 54981
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "KuarVtvnJSlZGhbLyJzDiUIsUKLAVdiQ"
app.config['MYSQL_DB'] = "railway"

mysql = MySQL(app)
app.secret_key = os.getenv('SECRET_KEY', 'mysecretkey')

# Ruta principal
@app.route('/')
def Index():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM beneficiario')
        data = cur.fetchall()
        return render_template('index.html', beneficiarios=data)
    except Exception as e:
        flash(f"Error al conectar con la base de datos: {str(e)}", "danger")
        return render_template('index.html', beneficiarios=[])

# Agregar beneficiario (sin hospital)
@app.route('/agregarBeneficiario', methods=['POST'])
def agregarBeneficiario():
    try:
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        dni = request.form.get('dni')

        if not nombre or not apellido or not dni:
            flash('Todos los campos son obligatorios.', 'warning')
            return redirect(url_for('Index'))

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO beneficiario (nombre, apellido, dni) VALUES (%s, %s, %s)',
                    (nombre, apellido, dni))
        mysql.connection.commit()
        flash('Beneficiario agregado con éxito', 'success')
    except Exception as e:
        flash(f"Error al agregar beneficiario: {str(e)}", 'danger')
    
    return redirect(url_for('Index'))

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
