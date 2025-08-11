import sqlite3

from flask import Flask, request, render_template, session, redirect

app = Flask(__name__)
app.secret_key = 'gfy&66*&dhefu'

SPEND = 1
INCOME = 2

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

@app.route('/dashboard')
def dashboard():
    if 'users_id' not in session:
        return redirect('/login')
    with Database('financial_tracker.db') as cursor:
        cursor.execute(
            'SELECT * FROM transactions WHERE owner =?',
            (session['users_id'],)
        )
        transactions = cursor.fetchall()
    return render_template('dashboard.html', transactions=transactions)



@app.route("/user", methods=['GET', 'POST'])
def user_handler():
    if request.method == 'GET':
        return "Hello World. GET"
    else:
        return 'Hello World POST'


@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        with Database('financial_tracker.db') as cursor:
            result = cursor.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password)
            )
            data = result.fetchone()
        if data:
            session['users_id'] = data[0]  # сохраняем id пользователя
            return 'correct user pair'
        else:
            return 'wrong user pair'


@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                "INSERT INTO users (name, surname, password, email) VALUES (?, ?, ?, ?)",
                (name, surname, password, email)
            )
        return 'user registered'


@app.route('/category', methods=['GET', 'POST'])
def get_category():
    if request.method == 'GET':
        return 'hello world GET'
    else:
        return 'hello world POST'


@app.route('/category/<category_id>', methods=['GET', 'PATCH', 'DELETE'])
def get_category_2(category_id):
    if request.method == 'GET':
        return f'this is category {category_id}'
    elif request.method == 'PATCH':
        return 'PATCH'
    else:
        return 'hello world DELETE'


@app.route('/income', methods=['GET', 'POST'])
def income():
    if 'users_id' not in session:
        return redirect('/login')
    if request.method == 'GET':
        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                "SELECT * FROM transactions WHERE owner = ? AND type = ?",
                (session['users_id'], INCOME)
            )
            res = cursor.fetchall()
            return render_template('dashboard.html', transactions=res)
    else:
        transactions_description = request.form['description']
        transactions_category = request.form['category']
        transactions_date = request.form['date']
        transactions_owner = session['users_id']  # берём из сессии
        transactions_type = INCOME
        transactions_amount = request.form['amount']

        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                "INSERT INTO transactions (description, category, date, owner, type, amount) VALUES (?, ?, ?, ?, ?, ?)",
                    (transactions_description, transactions_category, transactions_date, transactions_owner, transactions_type, transactions_amount)
            )
            return redirect('/income')



@app.route('/income/<income_id>', methods=['GET', 'PATCH', 'DELETE'])
def income_2(income_id):
    if request.method == 'GET':
        return f'this is income {income_id}'
    elif request.method == 'PATCH':
        return 'PATCH'
    else:
        return 'hello world DELETE'


@app.route('/spend', methods=['GET', 'POST'])
def spend():
    if 'users_id' not in session:
        return redirect('login')
    if request.method == 'GET':
        with Database('financial_tracker.db') as cursor:  # исправлено название файла
            cursor.execute(
                "SELECT * FROM transactions WHERE owner = ? AND type = ?",
                (session['users_id'], SPEND)
            )
            res = cursor.fetchall()
            return render_template('dashboard.html', transactions=res)
    else:
        transaction_description = request.form['description']
        transaction_category = request.form['category']
        transaction_date = request.form['date']
        transaction_owner = session['users_id']  # берём из сессии
        transaction_type = SPEND
        transaction_amount = request.form['amount']

        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                "INSERT INTO transactions (description, category, date, owner, type, amount) VALUES (?, ?, ?, ?, ?, ?)",
                (transaction_description, transaction_category, transaction_date, transaction_owner, transaction_type, transaction_amount)
            )
        return redirect('/spend')




@app.route('/spend/<spend_id>', methods=['GET', 'PATCH', 'DELETE'])
def spend_2(spend_id):
    if request.method == 'GET':
        return f'this is spend {spend_id}'
    elif request.method == 'PATCH':
        return 'PATCH'
    else:
        return 'hello world DELETE'


if __name__ == "__main__":
    app.run(debug=True)
