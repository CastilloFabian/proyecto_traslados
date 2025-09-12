import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos usando variables de entorno
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))  # Default a 3306
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

# Inicializar MySQL
mysql = MySQL(app)

# Clave secreta para sesiones
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM beneficiario')
        data = cur.fetchall()
        return render_template('index.html', beneficiarios=data)
    except Exception as e:
        return f"Error de conexión a la base de datos: {str(e)}", 500


@app.route('/agregarBeneficiario', methods=['POST'])
def agregarBeneficiario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        id_hospital = request.form['aux_nombre_hospital_vista']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO beneficiario (nombre, apellido, dni) VALUES (%s,%s,%s)',
                    (nombre, apellido, dni))
        mysql.connection.commit()

        flash('Beneficiario agregado con éxito')

        # Obtener el ID del beneficiario recién agregado
        id_beneficiario = cur.lastrowid

        if id_beneficiario:
            agregar_cama(id_hospital, id_beneficiario)

        return redirect(url_for('hospital', id=id_hospital))


@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_contact.html', contact=data)


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_apellido = request.form['apellido']
        nuevo_dni = request.form['dni']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE beneficiario
            SET nombre = %s,
                apellido = %s,
                dni = %s
            WHERE id_beneficiario = %s
        """, (nuevo_nombre, nuevo_apellido, nuevo_dni, id))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Index'))


@app.route('/delete/<id>/<id_hospital>')
def delete_beneficiario(id, id_hospital):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM camas WHERE id_beneficiario = %s', (id,))
    mysql.connection.commit()

    cur.execute('DELETE FROM beneficiario WHERE id_beneficiario = %s', (id,))
    mysql.connection.commit()

    flash('Contacto eliminado con éxito')
    return redirect(url_for('hospital', id=id_hospital))


@app.route('/hospital/<id>')
def hospital(id):
    cur = mysql.connection.cursor()

    cur.execute('SELECT * FROM hospitales WHERE id_hospital = %s', (id,))
    nombre_hospital = cur.fetchall()

    cur.execute('SELECT * FROM camas WHERE id_hospital = %s', (id,))
    data = cur.fetchall()

    data_beneficiario = []
    for bnf in data:
        id_beneficiario = bnf[2]
        cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s', (id_beneficiario,))
        beneficiario = cur.fetchone()
        if beneficiario:
            data_beneficiario.append(beneficiario)

    return render_template(
        'vista_hospital.html',
        datos=data,
        data_beneficiario_vista=data_beneficiario,
        nombre_hospital_vista=nombre_hospital
    )


# Función auxiliar para agregar una cama
def agregar_cama(id_hospital, id_beneficiario):
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO camas (id_hospital, id_beneficiario) VALUES (%s,%s)',
                (id_hospital, id_beneficiario))
    mysql.connection.commit()


# Ejecutar en local
if __name__ == '__main__':
    app.run(debug=True)
