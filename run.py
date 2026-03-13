from flask import Flask
from app.routes import main
from app.extensions import mail

app = Flask(__name__)
app.config.from_object("app.config")

mail.init_app(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
