from flask import Flask, render_template, request, redirect, session, url_for
from models import db, User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'ja'

db.init_app(app)

# ===================== LANDING PAGE =====================
@app.route('/landing')
def landing():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)