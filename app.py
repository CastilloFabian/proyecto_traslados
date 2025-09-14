import os
from flask import Flask, render_template, request, redirect, url_for, flash, g
import pymysql
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

# Clave secreta para sesiones
app.secret_key = os.getenv('SECRET_KEY', 'mysecretkey')

# Función para obtener conexión a base de datos usando PyMySQL
def get_db_connection():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor  # Retorna dicts en vez de tuplas
        )
    return g.db

# Cerrar conexión al terminar la request
@app.teardown_appcontext
def close_db_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Ruta principal: lista de beneficiarios
@app.route('/')
def Index():
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
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

            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO beneficiario (nombre, apellido, dni) VALUES (%s, %s, %s)',
                    (nombre, apellido, dni)
                )
                conn.commit()

                id_beneficiario = cur.lastrowid

            flash('Beneficiario agregado con éxito', 'success')

            if id_beneficiario:
                agregar_cama(id_hospital, id_beneficiario)

            return redirect(url_for('hospital', id=id_hospital))

        except Exception as e:
            flash(f"Error al agregar beneficiario: {str(e)}", 'danger')
            return redirect(url_for('Index'))

# Ruta para obtener datos de un beneficiario (para editar)
@app.route('/edit/<int:id>')
def get_contact(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s', (id,))
            data = cur.fetchone()
        return render_template('edit_contact.html', contact=data)
    except Exception as e:
        flash(f"Error al cargar datos del beneficiario: {str(e)}", 'danger')
        return redirect(url_for('Index'))

# Ruta para actualizar un beneficiario
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        try:
            nuevo_nombre = request.form['nombre']
            nuevo_apellido = request.form['apellido']
            nuevo_dni = request.form['dni']

            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE beneficiario
                    SET nombre = %s,
                        apellido = %s,
                        dni = %s
                    WHERE id_beneficiario = %s
                """, (nuevo_nombre, nuevo_apellido, nuevo_dni, id))
                conn.commit()

            flash('Contacto actualizado', 'success')
            return redirect(url_for('Index'))

        except Exception as e:
            flash(f"Error al actualizar contacto: {str(e)}", 'danger')
            return redirect(url_for('Index'))

# Ruta para eliminar un beneficiario
@app.route('/delete/<int:id>/<int:id_hospital>')
def delete_beneficiario(id, id_hospital):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('DELETE FROM camas WHERE id_beneficiario = %s', (id,))
            conn.commit()

            cur.execute('DELETE FROM beneficiario WHERE id_beneficiario = %s', (id,))
            conn.commit()

        flash('Contacto eliminado con éxito', 'success')
        return redirect(url_for('hospital', id=id_hospital))

    except Exception as e:
        flash(f"Error al eliminar contacto: {str(e)}", 'danger')
        return redirect(url_for('Index'))

# Vista de hospital (ver camas y beneficiarios asociados)
@app.route('/hospital/<int:id>')
def hospital(id):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Datos del hospital
            cur.execute('SELECT * FROM hospitales WHERE id_hospital = %s', (id,))
            nombre_hospital = cur.fetchone()

            # Datos de camas
            cur.execute('SELECT * FROM camas WHERE id_hospital = %s', (id,))
            camas = cur.fetchall()

            # Obtener datos de cada beneficiario asignado a cama
            data_beneficiario = []
            for bnf in camas:
                id_beneficiario = bnf['id_beneficiario']
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
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute('INSERT INTO camas (id_hospital, id_beneficiario) VALUES (%s, %s)',
                        (id_hospital, id_beneficiario))
            conn.commit()
    except Exception as e:
        flash(f"Error al asignar cama: {str(e)}", 'danger')

# Ejecutar en modo desarrollo, con puerto de Railway o 5000 por defecto
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
