from flask import Flask, render_template, request, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en variables de entorno")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        carnet = request.form['carnet']
        consume = request.form['consume']

        # Si no consume, solo guarda esa parte
        if consume == "No":
            data = {
                "nombre": nombre,
                "apellido": apellido,
                "edad": edad,
                "carnet": carnet,
                "consume": consume,
                "frecuencia": None,
                "tipos": None,
                "favorita": None
            }
        else:
            frecuencia = request.form.getlist('frecuencia')
            tipos = request.form.getlist('tipos')
            favorita = request.form['favorita']

            data = {
                "nombre": nombre,
                "apellido": apellido,
                "edad": edad,
                "carnet": carnet,
                "consume": consume,
                "frecuencia": ", ".join(frecuencia),
                "tipos": ", ".join(tipos),
                "favorita": favorita
            }

        supabase.table(SUPABASE_TABLE).insert(data).execute()
        return "✅ Encuesta enviada correctamente. ¡Gracias por participar!"

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
