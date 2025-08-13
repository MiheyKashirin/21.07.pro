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
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class DBwrapper:
    def insert(self, table, data):
        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                f"INSERT INTO {table}({','.join(data.keys())}) VALUES ({','.join(['?'] * len(data))})",
                tuple(data.values())
            )

    def select(self, table, where=None):
        with Database('financial_tracker.db') as cursor:
            if where:
                result_params = []
                for key, value in where.items():
                    if isinstance(value, list):
                        result_params.append(f"{key} IN ({','.join(str(v) for v in value)})")
                    else:
                        if isinstance(value, str):
                            result_params.append(f"{key} = '{value}'")
                        else:
                            result_params.append(f"{key} = {value}")
                result_where = ' AND '.join(result_params)
                cursor.execute(f"SELECT * FROM {table} WHERE {result_where}")
            else:
                cursor.execute(f"SELECT * FROM {table}")
            return cursor.fetchall()


@app.route('/dashboard')
def dashboard():
    if 'users_id' not in session:
        return redirect('/login')
    db = DBwrapper()
    res = db.select('transactions', {'owner': session['users_id']})
    return render_template('dashboard.html', transactions=res)


@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        db = DBwrapper()
        data = db.select('users', {'email': email, 'password': password})
        if data:
            session['users_id'] = data[0]['id']
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
        db = DBwrapper()
        db.insert('users', {'name': name, 'surname': surname, 'password': password, 'email': email})
        return 'user registered'


@app.route('/category', methods=['GET', 'POST'])
def get_category():
    if 'users_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            res = db.select('category', {'owner': [session['users_id'], 1]})
            return render_template('category_list.html', categories=res)
        else:
            category_name = request.form['category_name']
            category_owner = session['users_id']
            db.insert('category', {'name': category_name, 'owner': category_owner})
            return redirect('/category')


@app.route('/category/<category_id>', methods=['GET', 'POST'])
def get_category_2(category_id):
    if 'users_id' in session:
        db = DBwrapper()
        if request.method == 'GET':
            res = db.select('transactions', {'category': category_id, 'owner': session['users_id']})
            curr_category = db.select('category', {'id': category_id})[0]
            return render_template('one_category.html', transactions=res, category=curr_category)
        else:
            return 'hello world edit category'


@app.route('/income', methods=['GET', 'POST'])
def income():
    if 'users_id' not in session:
        return redirect('/login')
    db = DBwrapper()
    if request.method == 'GET':
        res = db.select('transactions', {'owner': session['users_id'], 'type': INCOME})
        return render_template('dashboard.html', transactions=res)
    else:
        db.insert('transactions', {
            'description': request.form['description'],
            'category': request.form['category'],
            'date': request.form['date'],
            'owner': session['users_id'],
            'type': INCOME,
            'amount': request.form['amount']
        })
        return redirect('/income')


@app.route('/spend', methods=['GET', 'POST'])
def spend():
    if 'users_id' not in session:
        return redirect('/login')
    db = DBwrapper()
    if request.method == 'GET':
        res = db.select('transactions', {'owner': session['users_id'], 'type': SPEND})
        return render_template('dashboard.html', transactions=res)
    else:
        db.insert('transactions', {
            'description': request.form['description'],
            'category': request.form['category'],
            'date': request.form['date'],
            'owner': session['users_id'],
            'type': SPEND,
            'amount': request.form['amount']
        })
        return redirect('/spend')


if __name__ == "__main__":
    app.run(debug=True)


