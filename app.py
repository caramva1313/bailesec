from flask import Flask, render_template, request
import sqlite3  # Para trabajar con la base de datos SQLite

app = Flask(__name__)  # Crea una instancia de la aplicación Flask

# Función para inicializar la base de datos SQLite y crear la tabla si no existe
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cedulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_cedula TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# Ruta principal para buscar cédulas
@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = ""
    if request.method == "POST":  # Comprueba si es una solicitud POST
        cedula = request.form.get("cedula")  # Obtiene la información enviada en el formulario
        if cedula:
            if buscar_cedula_en_db(cedula):
                mensaje = "Cédula encontradaaaaaaaaaaaaaaaa"
            else:
                mensaje = "Cédula no encontradaxxxxxxxxxxxxxxxxxxx"
    return render_template("index.html", mensaje=mensaje)


# Ruta para agregar cédulas manualmente
@app.route("/agregar_cedula", methods=["GET", "POST"])
def agregar_cedula():
    mensaje = ""
    if request.method == "POST":  # Procesar la solicitud POST
        cedula = request.form.get("cedula")
        if cedula:
            try:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO cedulas (numero_cedula) VALUES (?)", (cedula,))
                conn.commit()
                conn.close()
                mensaje = "Cédula agregada con éxito"
            except sqlite3.IntegrityError:
                mensaje = "La cédula ya existe en la base de datos"
    return render_template("agregar_cedula.html", mensaje=mensaje)


# Función para buscar una cédula en la base de datos
def buscar_cedula_en_db(cedula):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cedulas WHERE numero_cedula = ?", (cedula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


# Iniciar la base de datos
init_db()

if __name__ == "__main__":
    app.run(debug=True)

