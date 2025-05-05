from flask import Flask
from routes.summarize import summarize_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(summarize_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
