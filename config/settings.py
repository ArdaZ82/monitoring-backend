import os

# URL del servidor para pruebas locales o producción. 
# En Render.com, por ejemplo, se usaría la URL pública asignada.
SERVER_URL = "https://monitor-backend-wsot.onrender.com"

# Nombre de usuario que identifica al dispositivo (para el cliente)
USER_NAME = "Sebastian"

# Intervalo de captura en segundos (para el cliente)
CAPTURE_INTERVAL = 10

# Carpeta para almacenar capturas en el servidor.
# Se crea en el directorio actual, en una carpeta llamada "capturas".
UPLOAD_FOLDER = os.path.join(os.getcwd(), "capturas")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
