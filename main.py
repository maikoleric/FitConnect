from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB, Query
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skrivnost'

db = TinyDB('users.json')
User = Query()

@app.route('/')
def landing():
    quote_data = requests.get('https://zenquotes.io/api/random').json()
    quote = {
    'text': quote_data[0].get('q') or 'Vztrajaj, tudi ko je težko.',
    'author': quote_data[0].get('a') or 'Neznan'
}

    location_data = requests.get('https://ipapi.co/json/').json()
    city = location_data.get('city', 'neznano')
    country = location_data.get('country_name', 'neznano')

    return render_template('index.html', quote=quote, city=city, country=country)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db.insert({
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'age': int(request.form['age']),
            'experience': request.form['experience'],
            'split': request.form['split'],
            'gym_name': request.form['gym_name'],
            'location': request.form['location'],
            'password': request.form['password']
        })
        return redirect('/login')
    return render_template('register.html')