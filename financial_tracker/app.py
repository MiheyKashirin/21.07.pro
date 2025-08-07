import sqlite3

from flask import Flask, request, render_template


app = Flask(__name__)

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()



@app.route("/user", methods=['GET','POST'])
def user_handler():
    if request.method=='GET':
        return "HEllo World. GET"
    else:
        return 'hello world POST'


@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        with Database('financial_tracker.db') as cursor:
            result = cursor.execute(f'SELECT * FROM user where email = {email} and password {password}')
            data = result.fetchone()
        if data:
            return f'correct user pair'
        else:
            return f'wrong user pair'



@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method=='GET':
        return render_template('/register.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        email= request.form['email']
        with Database('financial_tracker.db') as cursor:
            cursor.execute(f"INSERT INTO users (name, surname,password, email) VALUES ({name},{surname},{password},{email})")
        return f'user registered'


@app.route('/category', methods=['GET', 'POST'])
def get_category():
    if request.method=='GET':
        return 'hello world GET'
    else:
        return 'hello world POST'


@app.route('/category/<category_id>', methods=['GET','PATCH','DELETE'])
def get_category_2(category_id):
    if request.method=='GET':
        return f'this is category {category_id}'
    elif request.method=='PATCH':
        return 'PATCH'
    else:
        return  'hello world DELETE'


@app.route('/income', methods=['GET','POST'])
def income():
    if request.method=='GET':
        return 'hello world GET'
    else:
        return 'hello world POST'


@app.route('/income/<income_id>', methods=['GET','PATCH','DELETE'])
def income_2(income_id):
    if request.method=='GET':
        return f'this is income {income_id}'
    elif request.method=='PATCH':
        return 'PATCH'
    else:
        return 'hello world DELETE'



@app.route('/spend', methods=['GET','POST'])
def spend():
    if request.method=='GET':
        return 'hello world GET'
    else:
        return 'hello world POST'



@app.route('/spend/<spend_id>', methods=['GET','PATCH','DELETE'])
def spend_2(spend_id):
    if request.method=='GET':
        return f'this is spend {spend_id}'
    elif request.method=='PATCH':
        return 'PATCH'
    else:
        return  'hello world DELETE'


if __name__== '__main__':
    app.run()


