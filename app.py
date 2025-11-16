import os
from flask_mysql_connector import MySQL
# from flask_mysqldb import MySQL
# from dotenv import load_dotenv

from flask import Flask, render_template
from mega import Mega

app = Flask(__name__)
# ////////////////////////////////////////////////////
# mysql
# //////////////////////////////////////////////////////
app.config['MYSQL_HOST']     = 'mysql-383b2079-fabianrmx-014d.b.aivencloud.com'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'defaultdb'
mysql = MySQL(app)

# //////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////
# --- Configuración de Mega ---
MEGA_EMAIL = "castillofabian.uep@gmail.com"
MEGA_PASSWORD = "--uep2024--"

# Conectarse a Mega (solo la app inicia sesión)
mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)
print(m)
# //////////////////////////////////////////////////////
#
# //////////////////////////////////////////////////////


# Lista de nombres de archivos que quieres mostrar
nombres_archivos = ["imagen1.jpg", "imagen1.pdf"]
archivos = []
print(archivos)

for nombre in nombres_archivos:
    archivo = m.find(nombre)  # Buscar el archivo en tu cuenta
    if archivo:
        enlace = m.get_link(archivo)  # Generar enlace público
        archivos.append({'nombre': nombre, 'enlace': enlace})
        print(f"Archivo {nombre} ENCONTRADO")
    else:
        print(f"Archivo {nombre} no encontrado")

print("---------------------------------------------------")
print(archivos)
print("---------------------------------------------------")

@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM beneficiario")
    beneficiarios = cur.fetchall()
    # Pasamos solo el nombre y el enlace público a la vista
    return render_template("index.html",archivos=archivos ,beneficiarios=beneficiarios)

# funciona para local
if __name__ == "__main__":
    app.run(debug=True)

#funciona para render
# if __name__ == "__main__":
#     app.run()