import sqlite3



from flask import Flask, request, render_template, session, redirect
import models
from sqlalchemy import select

from dataBase import db_session, init_db


app = Flask(__name__)
app.secret_key = 'gfy&66*&dhefu'

SPEND = 'spend'
INCOME = 'income'



@app.route('/dashboard')
def dashboard():
    if 'users_id' not in session:
        return redirect('/login')
    transactions = list(db_session.execute(select(models.Transactions).filter_by(owner=session['users_id'])).scalars())
    return render_template('dashboard.html', transactions=transactions)



@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        init_db()
        data = list(db_session.execute(select(models.Users).filter_by(email=email, password=password)).scalars())

    if data:
            session['users_id'] = data[0].id
            return 'correct user pair'
    return f"wrong user pair"


@app.route('/register', methods=['GET', 'POST'])
def get_register(new_user=None):
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        init_db()
        next_user= models.Users(name=name, surname=surname, password= password,email=email)
        db_session.add(next_user)
        db_session.commit()
        return 'user registered'


@app.route('/category', methods=['GET', 'POST'])
def get_category():
    if 'users_id' in session:
        if request.method == 'GET':
            init_db()
            categories = list(db_session.execute(select(models.Category).filter_by(owner=session['users_id'])).scalars())
            categories_system = list(
                db_session.execute(select(models.Category).filter_by(owner=1)).scalars())
            return render_template('category_list.html',categories=categories + categories_system)
        else:
            category_name = request.form['category_name']
            category_owner = session['users_id']
            new_category = models.Category(name=category_name, owner=category_owner)
            db_session.add(new_category)
            db_session.commit()
            return redirect('/category')
    else:

        return redirect('/login')




@app.route('/category/<category_id>', methods=['GET', 'POST'])
def get_category_2(category_id):
    if 'users_id' in session:
        if request.method == 'GET':
            transactions= list(db_session.execute(select(models.Transactions).filter_by(owner=session['users_id'], category=category_id)).scalars())
            curr_category = db_session.execute(select(models.Category).filter_by(id=category_id)).scalars().first()
            return render_template('one_category.html', transactions=transactions, category=curr_category)
        else:
            return 'hello world edit category'


@app.route('/income', methods=['GET', 'POST'])
def income():
    if 'users_id' not in session:
        return redirect('/login')

    if request.method == 'GET':
        transactions = list(db_session.execute(select(models.Transactions).filter_by(owner=session['users_id'], type=INCOME)).scalars())
        return render_template('dashboard.html', transactions=transactions)

    else:
        new_transaction = models.Transactions(
            description=request.form['description'],
            category=request.form['category'],
            date=request.form['date'],
            owner=session['users_id'],
            type=INCOME,
            amount=request.form['amount']
        )
        db_session.add(new_transaction)
        db_session.commit()
        return redirect('/income')


@app.route('/spend', methods=['GET', 'POST'])
def spend():
    if 'users_id' not in session:
        return redirect('/login')

    if request.method == 'GET':
        transactions = list(db_session.execute(select(models.Transactions).filter_by(owner=session['users_id'], type=SPEND)).scalars())
        return render_template('dashboard.html', transactions=transactions)

    else:
        new_transaction = models.Transactions(
            description=request.form['description'],
            category=request.form['category'],
            date=request.form['date'],
            owner=session['users_id'],
            type=SPEND,
            amount=request.form['amount']
        )
        db_session.add(new_transaction)
        db_session.commit()
        return redirect('/spend')


if __name__ == "__main__":
    app.run(debug=True)


