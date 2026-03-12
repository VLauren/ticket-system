from flask import Flask
from flask_mail import Mail
from app.routes import main

app = Flask(__name__)
app.config.from_object("app.config")

mail = Mail(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
