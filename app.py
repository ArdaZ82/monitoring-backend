from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from datetime import datetime
from flask_cors import CORS

# Importar configuraciones globales
from config.settings import SERVER_URL, UPLOAD_FOLDER

app = Flask(__name__)
CORS(app)  # Permite peticiones desde otros orígenes

# Diccionario para almacenar las capturas organizadas por usuario (device_id)
user_captures = {}

@app.route("/upload", methods=["POST"])
def upload_screenshot():
    """
    Recibe la captura enviada por el cliente y la guarda en una carpeta
    específica según el identificador (device_id) enviado en la solicitud.
    """
    # Verificar que se envíe el archivo
    if "file" not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files["file"]
    # Obtener el identificador del dispositivo; si no se envía, usar "unknown"
    device_id = request.form.get("device_id", "unknown")
    
    # Crear la carpeta para este dispositivo si no existe
    device_folder = os.path.join(UPLOAD_FOLDER, device_id)
    os.makedirs(device_folder, exist_ok=True)
    
    # Crear un nombre único usando la fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    file_path = os.path.join(device_folder, filename)
    file.save(file_path)
    
    # Guardar la ruta relativa en el diccionario
    relative_path = os.path.join(device_id, filename)
    if device_id not in user_captures:
        user_captures[device_id] = []
    user_captures[device_id].append(relative_path)
    
    return jsonify({"message": "Captura recibida", "file_path": relative_path}), 200

@app.route("/captures/<user>", methods=["GET"])
def get_captures(user):
    """
    Devuelve un listado en JSON de todas las capturas almacenadas para un usuario (device_id).
    """
    if user not in user_captures:
        return jsonify({"error": "No hay imágenes para este usuario"}), 404
    return jsonify({"user": user, "captures": user_captures[user]})

@app.route("/view/<path:filename>", methods=["GET"])
def view_file(filename):
    """
    Sirve la imagen solicitada desde la carpeta de capturas.
    """
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/user/<username>")
def user_page(username):
    """
    Renderiza una página HTML que muestra todas las capturas asociadas a un usuario.
    (Esta ruta es opcional y sirve para que Cristian pueda visualizar las imágenes).
    """
    if username not in user_captures:
        return f"Usuario {username} no encontrado", 404
    # Se espera que la plantilla 'user.html' esté en la carpeta templates
    return render_template("user.html", user=username, captures=user_captures[username], server_url=SERVER_URL)

if __name__ == "__main__":
    # Ejecuta la aplicación en todas las interfaces, puerto 5000 y modo debug activado para desarrollo.
    app.run(host="0.0.0.0", port=5000, debug=True)
