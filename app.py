from flask import Flask, render_template, request, redirect, url_for
from Database import ensure_users_table, create_user, verify_user

app = Flask(__name__)

ensure_users_table()


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password_hash'].strip()

        success, result = create_user(email, password)

        if success:
            return redirect(url_for('login'))
        else:
            return result

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password_hash'].strip()

        success, result = verify_user(email, password)

        if success:
            username = result
            return f"Welcome {username}! Login successful"
        else:
            return result

    return render_template('login.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        trip_type = request.form['trip_type']
        from_country = request.form['from_country']
        to_country = request.form['to_country']
        depart_date = request.form['depart_date']
        return_date = request.form['return_date']
        travellers = request.form['travellers']

        print(trip_type, from_country, to_country, depart_date, return_date, travellers)
        return "Search data received!"

    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)