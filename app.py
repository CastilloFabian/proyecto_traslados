import os
from flask_mysql_connector import MySQL
from flask import Flask, render_template
from mega import Mega

app = Flask(__name__)

# ----------------------------------------
# CONFIGURACIÓN MYSQL (IMPORTANTE PARA RENDER)
# ----------------------------------------
app.config['MYSQL_HOST']     = 'mysql-383b2079-fabianrmx-014d.b.aivencloud.com'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'AVNS_crqvNWGBbCnEeSS0FeV'  # <- pon aquí tu PASS REAL
app.config['MYSQL_DATABASE'] = 'defaultdb'
app.config['MYSQL_POOL_NAME'] = 'pool1'
app.config['MYSQL_POOL_SIZE'] = 5

mysql = MySQL(app)

# ----------------------------------------
# CONFIG MEGA
# ----------------------------------------
MEGA_EMAIL = "castillofabian.uep@gmail.com"
MEGA_PASSWORD = "--uep2024--"

# Esta función maneja MEGA cuando la necesites
def obtener_archivos_mega():
    mega = Mega()

    try:
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
    except Exception as e:
        print("ERROR iniciando sesión en MEGA:", e)
        return []

    nombres_archivos = ["imagen1.jpg", "imagen1.pdf"]
    archivos = []

    for nombre in nombres_archivos:
        try:
            archivo = m.find(nombre)
            if archivo:
                enlace = m.get_link(archivo)
                archivos.append({'nombre': nombre, 'enlace': enlace})
        except:
            pass

    return archivos


# ----------------------------------------
# RUTAS
# ----------------------------------------
@app.route("/")
def index():
    # Obtener beneficiarios desde MySQL
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM beneficiario")
        beneficiarios = cur.fetchall()
    except Exception as e:
        print("ERROR MySQL:", e)
        beneficiarios = []

    # Obtener archivos desde MEGA SIN BLOQUEAR EL SERVIDOR
    archivos = obtener_archivos_mega()

    return render_template("index.html", archivos=archivos, beneficiarios=beneficiarios)


# ----------------------------------------
# EJECUTAR EN RENDER
# ----------------------------------------
if __name__ == "__main__":
    app.run()
