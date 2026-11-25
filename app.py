from flask import Flask, render_template, request
import sqlite3
import html

app = Flask(__name__)
DB_NAME = "lab_seguridad.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            rol TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    # Datos de prueba para el laboratorio
    usuarios_demo = [
        ("admin", "Administrador", "admin@universidad.local"),
        ("profesor", "Docente", "profesor@universidad.local"),
        ("estudiante1", "Alumno", "alumno1@universidad.local"),
        ("estudiante2", "Alumno", "alumno2@universidad.local")
    ]
    cursor.executemany("INSERT INTO usuarios (usuario, rol, email) VALUES (?, ?, ?)", usuarios_demo)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

# ==========================================
# ESCENARIO 1: INYECCIÓN SQL (SQLi)
# ==========================================
@app.route("/sqli", methods=["GET"])
def sqli():
    tipo = request.args.get("tipo", "vulnerable")
    query_param = request.args.get("usuario", "")
    consulta_ejecutada = ""
    resultados = []
    error = None

    if query_param:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            if tipo == "vulnerable":
                # PATRÓN INSEGURO: Concatenación directa de entradas de usuario
                consulta_ejecutada = f"SELECT id, usuario, rol, email FROM usuarios WHERE usuario = '{query_param}'"
                cursor.execute(consulta_ejecutada)
                resultados = cursor.fetchall()
            else:
                # PATRÓN SEGURO: Parámetros preparados (Prepared Statements)
                consulta_ejecutada = "SELECT id, usuario, rol, email FROM usuarios WHERE usuario = ?"
                cursor.execute(consulta_ejecutada, (query_param,))
                resultados = cursor.fetchall()
        except sqlite3.Error as e:
            error = str(e)
        finally:
            conn.close()

    return render_template(
        "sqli.html",
        tipo=tipo,
        usuario=query_param,
        consulta_ejecutada=consulta_ejecutada,
        resultados=resultados,
        error=error
    )

# ==========================================
# ESCENARIO 2: CROSS-SITE SCRIPTING (XSS)
# ==========================================
@app.route("/xss", methods=["GET"])
def xss():
    tipo = request.args.get("tipo", "vulnerable")
    mensaje = request.args.get("mensaje", "")
    contenido_renderizado = ""

    if mensaje:
        if tipo == "vulnerable":
            # PATRÓN INSEGURO: Se permite que el navegador interprete directamente texto sin sanear
            contenido_renderizado = mensaje
        else:
            # PATRÓN SEGURO: Escape de entidades HTML antes de la presentación
            contenido_renderizado = html.escape(mensaje)

    return render_template(
        "xss.html",
        tipo=tipo,
        mensaje=mensaje,
        contenido_renderizado=contenido_renderizado
    )

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.")
    print("Iniciando servidor de laboratorio local en http://127.0.0.1:5000 ...")
    app.run(debug=True, host="127.0.0.1", port=5000)
