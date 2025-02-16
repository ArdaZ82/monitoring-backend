from flask import Flask
from routes import web

app = Flask(__name__)
app.register_blueprint(web)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Puedes elegir otro puerto si es necesario
