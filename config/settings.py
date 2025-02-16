import os

# URL del servidor en producción (Render.com)
SERVER_URL = "https://monitor-backend-wsot.onrender.com"

# Nombre de usuario (si se usa en el cliente)
USER_NAME = "Sebastian"

# Intervalo de captura (usado en el cliente, por ejemplo)
CAPTURE_INTERVAL = 10


# BASE DE DATOS
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin_monitor:HqjQQ7WaTXdJqq64ufVuaiFupxCM9PSD@dpg-cup21pdumphs73e2sfjg-a/monitoring_system_lq1r")

# Carpeta para almacenar las capturas en el servidor.
# Se creará en el directorio actual, en una carpeta llamada "capturas".
UPLOAD_FOLDER = os.path.join(os.getcwd(), "capturas")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
