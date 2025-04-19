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
    return render_template('index.html', quote=quote)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.search(
            (User.first_name == request.form['first_name']) &
            (User.last_name == request.form['last_name']) &
            (User.password == request.form['password'])
        )
        if user:
            session['user'] = user[0]
            return redirect('/users')
        return "Napaka pri prijavi."
    return render_template('login.html')

@app.route('/users')
def users():
    if 'user' not in session:
        return redirect('/login')
    return render_template('users.html', users=db.all())

if __name__ == '__main__':
    app.run(debug=True)
