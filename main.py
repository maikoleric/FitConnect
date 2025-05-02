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
            'password': request.form['password'],
            'contact' : request.form['contact']
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
            return redirect('/dashboard')
        return "Napaka pri prijavi."
    return render_template('login.html')

@app.route('/users',methods=['GET', 'POST'])
def users():
    if 'user' not in session:
        return redirect('/login')
    all_users = db.all()

    if request.method == 'POST':
        selected_split = request.form.get('split')
        selected_location = request.form.get('location')
        selected_age = request.form.get('age')
        filtered_users = all_users
        
        if selected_split:
           new_list = []
        for user in filtered_users:
                if user['split'] == selected_split:
                    new_list.append(user)
        filtered_users = new_list

        if selected_location:
            new_list = []
            for user in filtered_users:
                if user['location'] == selected_location:
                    new_list.append(user)
            filtered_users = new_list 

        if selected_age:
            new_list = []
        for user in filtered_users:
            age = user['age']
        if selected_age == '14-18':
            if age >= 14 and age <= 18:
                new_list.append(user)
        if selected_age == '18-25':
            if age > 18 and age <= 25:
                new_list.append(user)
        if selected_age == '25+':
            if age > 25:
                new_list.append(user)
        filtered_users = new_list

        return render_template('users.html', users=filtered_users)
    return render_template('users.html', users=all_users)


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    user = session['user']
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
