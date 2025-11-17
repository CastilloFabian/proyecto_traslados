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
@app.route("/mega")
def mega_route():
    MEGA_EMAIL = "castillofabian.uep@gmail.com"
    MEGA_PASSWORD = "--uep2024--"

    mega = Mega()
    try:
        m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    nombres = ["imagen1.jpg", "imagen1.pdf"]
    archivos = []

    for n in nombres:
        arch = m.find(n)
        if arch:
            archivos.append({"nombre": n, "enlace": m.get_link(arch)})

    return jsonify(archivos)


# ----------------------------------------
# EJECUTAR EN RENDER
# ----------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
