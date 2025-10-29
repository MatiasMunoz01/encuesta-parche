from flask import Flask, render_template, request, jsonify
from supabase import create_client
import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "bebidas_encuesta")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltan SUPABASE_URL o SUPABASE_KEY en variables de entorno")

# Crear cliente Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        carnet = request.form.get('carnet', '').strip()
        edad_raw = request.form.get('edad', '')
        edad = int(edad_raw) if edad_raw.isdigit() else None

        consume = request.form.get('consume', 'No')

        if consume.lower() != "sí" and consume.lower() != "si":
            # Si no consume, guardamos solo los datos básicos
            data = {
                "nombre": nombre,
                "apellido": apellido,
                "carnet": carnet,
                "edad": edad,
                "consume": False,
                "frecuencia": None,
                "tipos": None,
                "favorita": None
            }
        else:
            # Si sí consume, recogemos lo demás
            # frecuencia y tipos pueden venir como múltiple (lista)
            frecuencia_list = request.form.getlist('frecuencia')
            tipos_list = request.form.getlist('tipos')
            favorita = request.form.get('favorita', '').strip()

            data = {
                "nombre": nombre,
                "apellido": apellido,
                "carnet": carnet,
                "edad": edad,
                "consume": True,
                "frecuencia": ", ".join(frecuencia_list) if frecuencia_list else None,
                "tipos": ", ".join(tipos_list) if tipos_list else None,
                "favorita": favorita or None
            }

        # Insertar en Supabase
        response = supabase.table(SUPABASE_TABLE).insert(data).execute()
        # Opcional: puedes revisar response for debugging
        # print("Supabase response:", response)

        return "✅ Encuesta enviada correctamente. ¡Gracias por participar!"
    except Exception as e:
        # Devuelve error en JSON para facilitar debug
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Elegir puerto dinámico para Render o usar 5000 localmente
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
