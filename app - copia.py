from flask import Flask, render_template , request,redirect ,url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'traslados_bd'
mysql = MySQL(app)

# setting
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM beneficiario')
    data = cur.fetchall()
    return render_template('index.html' , beneficiarios = data)

@app.route('/agregarBeneficiario', methods=['POST'])  # 'methods', no 'method'
def agregarBeneficiario():
    if request.method == 'POST':  # Correcto: 'method', no 'metod'
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        id_hospital = request.form['aux_nombre_hospital_vista']

        # Aquí puedes continuar con el procesamiento de los datos
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO beneficiario (nombre, apellido, dni) VALUES (%s,%s,%s)',(nombre, apellido, dni))
        mysql.connection.commit()
        flash('Beneficiario agregado con exito')

        # busco el id_beneficiario de la tabla BENEFICIARIO mediante le DNI
        cur.execute('SELECT * FROM beneficiario WHERE dni = %s',(dni,))
        beneficiario = cur.fetchall()

        id_beneficiario = 0
        print(" INFORMACION DE BENEFICIARIO")
        print(beneficiario)
        for dato in beneficiario:
            id_beneficiario = dato[0]
        print(" INFORMACION DE BENEFICIARIO")
        
        print("*******************************************")
        print(id_hospital)
        print(id_beneficiario)
        print("*******************************************")
        
        agregar_cama(id_hospital,id_beneficiario)
        # return redirect(url_for('Index'))
        return redirect(url_for('hospital',id=id_hospital))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s', (id,))
    data = cur.fetchall()
    return render_template('edit_contact.html', contact = data)

@app.route('/update/<id>', methods= ['POST'])
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
        """, (nuevo_nombre,nuevo_apellido,nuevo_dni,id))
        mysql.connection.commit()
        flash('contacto actualizado')
        return redirect(url_for('hospital'))

@app.route('/delate/<id>,<id_hospital>')
def delate_beneficiario(id,id_hospital):
    cur = mysql.connection.cursor()

    cur.execute('DELETE FROM camas WHERE id_beneficiario = %s', (id,))
    mysql.connection.commit()

    cur.execute('DELETE FROM beneficiario WHERE id_beneficiario =  %s', (id,))
    mysql.connection.commit()

    flash('Contacto eliminado con exito')
    return redirect(url_for('hospital',id = id_hospital))

# vista hospital : Muesta la vista principal que muestra los BNF 
@app.route('/hospital/<id>')
def hospital(id):
    cur = mysql.connection.cursor()

    # se obtien el NOMBRE DE HOSPITAL para mostrarlo en la vista
    cur.execute('SELECT * FROM hospitales WHERE id_hospital = %s', (id,))
    nombre_hospital = cur.fetchall()
    print(nombre_hospital)

    # Se obtiene los valores de las CAMAS que estan en el hospital pasado como parametro
    cur.execute('SELECT * FROM camas WHERE id_hospital = %s', (id,))
    data = cur.fetchall()
    
    # se obtiene los BENEFICIARIOS que estaban en la tabla de camas 
    data_beneficiario = ()
    for bnf in data:
        # obtengo el id_beneficiario cada registro de de la tabla camas 
        aux = bnf[2]
        # con ese valor busco en la tabla beneficiario
        cur.execute('SELECT * FROM beneficiario WHERE id_beneficiario = %s',(aux,))
        data_beneficiario = cur.fetchall() + data_beneficiario
    return render_template('vista_hospital.html', datos = data, data_beneficiario_vista = data_beneficiario, nombre_hospital_vista = nombre_hospital)

# AGRAGAR CAMA
@app.route('/agregar_cama')
def agregar_cama(id_hospital,id_beneficiario):
    id_hospital=1
    id_beneficiario = id_beneficiario
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO camas (id_hospital,id_beneficiario) VALUES (%s,%s)',(id_hospital,id_beneficiario))
    cur.connection.commit()
    # flash('se agrego la cama con exito')
    return 0


if __name__ == '__main__':
    app.run(port=3000, debug = True)
