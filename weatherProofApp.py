from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    temperature_threshold = db.Column(db.Integer, default=60)

    def __repr__(self) -> str:
        return f"User: {self.username} with temperature threshold: {self.temperature_threshold}"
    

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

app.run()