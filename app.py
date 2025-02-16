from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# Configuración de la aplicación
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "supersecretkey"
CORS(app)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin_monitor:HqjQQ7WaTXdJqq64ufVuaiFupxCM9PSD@dpg-cup21pdumphs73e2sfjg-a.oregon-postgres.render.com/monitoring_system_lq1r"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Modelos de la base de datos
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # Puede ser "admin" o "user"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}, Role: {self.role}>"

class Capture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Capture {self.id}, User: {self.user_id}>"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.id}, User: {self.user_id}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rutas de autenticación
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin_panel"))
        
        return "Usuario o contraseña incorrectos", 401
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Ruta del panel de administración
@app.route("/admin")
@login_required
def admin_panel():
    if current_user.role != "admin":
        return "Acceso denegado: Se requiere permiso de administrador", 403
    return render_template("admin_panel.html")

# Subida de capturas de pantalla
@app.route("/upload", methods=["POST"])
def upload_screenshot():
    if "file" not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    file = request.files["file"]
    user_id = request.form.get("user_id")

    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Usuario no válido"}), 400

    user_folder = os.path.join("uploads", str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    file_path = os.path.join(user_folder, filename)
    file.save(file_path)

    new_capture = Capture(user_id=int(user_id), file_path=file_path)
    db.session.add(new_capture)
    db.session.commit()

    return jsonify({"message": "Captura guardada", "file_path": file_path}), 200

# Obtener capturas de un usuario
@app.route("/captures/<int:user_id>")
@login_required
def get_captures(user_id):
    if current_user.role != "admin":
        return "Acceso denegado: Se requiere permiso de administrador", 403
    captures = Capture.query.filter_by(user_id=user_id).all()
    return jsonify({"user_id": user_id, "captures": [c.file_path for c in captures]})

# Enviar notificaciones
@app.route("/send_notification", methods=["POST"])
@login_required
def send_notification():
    user_id = request.form.get("user_id")
    message = request.form.get("message")

    if not user_id or not message:
        return jsonify({"error": "Faltan datos: 'user_id' y 'message' son requeridos"}), 400

    new_notification = Notification(user_id=user_id, message=message)
    db.session.add(new_notification)
    db.session.commit()

    return jsonify({"message": f"Notificación enviada a {user_id}."}), 200

# Obtener notificaciones de un usuario
@app.route("/notifications/<int:user_id>")
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id).all()
    return jsonify({"user_id": user_id, "notifications": [n.message for n in notifications]})

# Otras rutas protegidas
@app.route("/captures")
@login_required
def captures():
    return render_template("captures.html")

@app.route("/tasks")
@login_required
def tasks():
    return render_template("tasks.html")

@app.route("/users")
@login_required
def users_list():
    users = User.query.all()
    return render_template("users.html", users=users)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
