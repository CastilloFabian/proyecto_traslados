import os
from flask import Flask, render_template, jsonify
from flask_mysql_connector import MySQL
from mega import Mega

app = Flask(__name__)

# ----------------------------------------
# CONFIG MYSQL (CORREGIDO)
# ----------------------------------------
app.config['MYSQL_HOST'] = 'mysql-383b2079-fabianrmx-014d.b.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_crqvNWGBbCnEeSS0FeV'
app.config['MYSQL_DATABASE'] = 'defaultdb'
app.config['MYSQL_PORT'] = 26821

# nombre corto para evitar el error
app.config['MYSQL_POOL_NAME'] = 'p1'
app.config['MYSQL_POOL_SIZE'] = 5

# SSL Aiven
app.config['MYSQL_SSL_CA'] = 'ca.pem'
app.config['MYSQL_SSL_DISABLED'] = False

mysql = MySQL(app)


# ----------------------------------------
# RUTA PRINCIPAL
# ----------------------------------------
@app.route("/")
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM beneficiario")
        beneficiarios = cur.fetchall()
    except Exception as e:
        print("ERROR MySQL:", e)
        beneficiarios = []

    return render_template("index.html", beneficiarios=beneficiarios)


# ----------------------------------------
# RUTA PARA MEGA
# ----------------------------------------
@app.route("/mega/<nombre_archivo>")
def mega_route(nombre_archivo):
    MEGA_EMAIL = "castillofabian.uep@gmail.com"
    MEGA_PASSWORD = "--uep2024--"

    mega = Mega()

    try:
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
    except Exception as e:
        return f"Error al iniciar sesión en MEGA: {e}", 500

    nombre_archivo = nombre_archivo + ".pdf"

    archivo = m.find(nombre_archivo)

    if not archivo:
        return f"No se encontró el archivo: {nombre_archivo}", 404

    enlace = m.get_link(archivo)

    # Renderiza una página que luego hace redirect desde el navegador
    return render_template("abrir_mega.html", enlace=enlace)
    #-------------------------


# ----------------------------------------
# EJECUTAR EN RENDER
# ----------------------------------------
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    app.run(debug=True)
