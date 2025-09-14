import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos usando variables de entorno

app.config['MYSQL_HOST'] = "centerbeam.proxy.rlwy.net"
app.config['MYSQL_PORT'] = 54981
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "KuarVtvnJSlZGhbLyJzDiUIsUKLAVdiQ"
app.config['MYSQL_DB'] = "railway"

# Inicializar MySQL
mysql = MySQL(app)

# Clave secreta para sesiones
app.secret_key = os.getenv('SECRET_KEY', 'mysecretkey')


# Ruta principal: lista de beneficiarios
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


# Ruta para agregar beneficiario
@app.route('/agregarBeneficiario', methods=['POST'])
def agregarBeneficiario():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            dni = request.form['dni']
            id_hospital = request.form['aux_nombre_hospital_vista']

            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO beneficiario (nombre, apellido, dni) VALUES (%s, %s, %s)',
                        (nombre, apellido, dni))
            mysql.connection.commit()

            flash('Beneficiario agregado con éxito', 'success')

            # Obtener ID del beneficiario recién agregado
            id_beneficiario = cur.lastrowid

            if id_beneficiario:
                agregar_cama(id_hospital, id_beneficiario)

            return redirect(url_for('hospital', id=id_hospital))

        except Exception as e:
            flash(f"Error al agregar beneficiario: {str(e)}", 'danger')
            return redirect(url_for('Index'))


# Ruta para obtener datos de un beneficiario (para editar)
@app.route('/edit/<id>')
def get_contact(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s', (id,))
        data = cur.fetchone()
        return render_template('edit_contact.html', contact=data)
    except Exception as e:
        flash(f"Error al cargar datos del beneficiario: {str(e)}", 'danger')
        return redirect(url_for('Index'))


# Ruta para actualizar un beneficiario
@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        try:
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

            flash('Contacto actualizado', 'success')
            return redirect(url_for('Index'))

        except Exception as e:
            flash(f"Error al actualizar contacto: {str(e)}", 'danger')
            return redirect(url_for('Index'))


# Ruta para eliminar un beneficiario
@app.route('/delete/<id>/<id_hospital>')
def delete_beneficiario(id, id_hospital):
    try:
        cur = mysql.connection.cursor()

        # Eliminar cama asociada
        cur.execute('DELETE FROM camas WHERE id_beneficiario = %s', (id,))
        mysql.connection.commit()

        # Eliminar beneficiario
        cur.execute('DELETE FROM beneficiario WHERE id_beneficiario = %s', (id,))
        mysql.connection.commit()

        flash('Contacto eliminado con éxito', 'success')
        return redirect(url_for('hospital', id=id_hospital))

    except Exception as e:
        flash(f"Error al eliminar contacto: {str(e)}", 'danger')
        return redirect(url_for('Index'))


# Vista de hospital (ver camas y beneficiarios asociados)
@app.route('/hospital/<id>')
def hospital(id):
    try:
        cur = mysql.connection.cursor()

        # Datos del hospital
        cur.execute('SELECT * FROM hospitales WHERE id_hospital = %s', (id,))
        nombre_hospital = cur.fetchone()

        # Datos de camas
        cur.execute('SELECT * FROM camas WHERE id_hospital = %s', (id,))
        camas = cur.fetchall()

        # Obtener datos de cada beneficiario asignado a cama
        data_beneficiario = []
        for bnf in camas:
            id_beneficiario = bnf[2]
            cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s', (id_beneficiario,))
            beneficiario = cur.fetchone()
            if beneficiario:
                data_beneficiario.append(beneficiario)

        return render_template(
            'vista_hospital.html',
            datos=camas,
            data_beneficiario_vista=data_beneficiario,
            nombre_hospital_vista=nombre_hospital
        )

    except Exception as e:
        flash(f"Error al cargar hospital: {str(e)}", 'danger')
        return redirect(url_for('Index'))


# Función auxiliar para agregar una cama
def agregar_cama(id_hospital, id_beneficiario):
    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO camas (id_hospital, id_beneficiario) VALUES (%s, %s)',
                    (id_hospital, id_beneficiario))
        mysql.connection.commit()
    except Exception as e:
        flash(f"Error al asignar cama: {str(e)}", 'danger')


# Ejecutar en modo desarrollo
if __name__ == '__main__':
    app.run(debug=True)
