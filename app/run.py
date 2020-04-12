from flask import Flask
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

from app.main.routes import main

app.register_blueprint(main)

if __name__=="__main__":
    app.run(debug=True)