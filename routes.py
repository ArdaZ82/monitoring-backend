from flask import Blueprint, render_template
import requests
from config.settings import SERVER_URL  # Asegúrate de que SERVER_URL esté definido en config/settings.py

web = Blueprint('web', __name__, template_folder='templates')

@web.route('/dashboard')
def dashboard():
    # Para este ejemplo, usaremos "Sebastian" como identificador (que es el device_id o nombre asignado)
    user = "Sebastian"
    try:
        # Llamamos al endpoint del servidor que devuelve las capturas del usuario
        response = requests.get(f"{SERVER_URL}/captures/{user}")
        if response.status_code == 200:
            data = response.json()
            captures = data.get("captures", [])
        else:
            captures = []
    except Exception as e:
        captures = []
    return render_template("user.html", user=user, captures=captures, server_url=SERVER_URL)
