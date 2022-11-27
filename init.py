from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:leisuregurube@localhost:5432/Airport"
CORS(app)

db = SQLAlchemy(app)
