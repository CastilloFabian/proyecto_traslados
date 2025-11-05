from flask import Flask, render_template
from mega import Mega

app = Flask(__name__)

# --- Configuración de Mega ---
MEGA_EMAIL = "castillofabian.uep@gmail.com"
MEGA_PASSWORD = "-uep2024-"

# Conectarse a Mega (solo la app inicia sesión)
mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

# Lista de nombres de archivos que quieres mostrar
nombres_archivos = ["imagen1.jpg", "archivo2.jpg"]
archivos = []

for nombre in nombres_archivos:
    archivo = m.find(nombre)  # Buscar el archivo en tu cuenta
    if archivo:
        enlace = m.get_link(archivo)  # Generar enlace público
        archivos.append({'nombre': nombre, 'enlace': enlace})
    else:
        print(f"Archivo {nombre} no encontrado")

@app.route("/")
def index():
    # Pasamos solo el nombre y el enlace público a la vista
    return render_template("index.html", archivos=archivos)

# funciona para local
# if __name__ == "__main__":
#     app.run(debug=True)

#funciona para render
if __name__ == "__main__":
    app.run()