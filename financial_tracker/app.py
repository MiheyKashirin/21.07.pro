import sqlite3
from flask import Flask, request, render_template, session, redirect
from sqlalchemy.sql.functions import aggregate_strings


import models
from sqlalchemy import select, or_, func, desc
from dataBase import db_session
from dataBase import init_db



from datetime import datetime

app = Flask(__name__)
app.secret_key = 'gfy&66*&dhefu'

SPEND = 'spend'
INCOME = 'income'


@app.route('/user', methods=['GET'])
def user_handler():
    if 'user_id' in session:
        stmt = select(models.Transactions).filter_by(owner=session['user_id'])
        if 'date_from' in request.args and 'date_to' in request.args:
            date_form = datetime.strptime(request.args['date_from'], '%Y-%m-%dT%H:%M')
            date_to = datetime.strptime(request.args['date_to'], '%Y-%m-%dT%H:%M')
            stmt = stmt.filter(models.Transactions.datetime.between(date_form,date_to))
        stmt = stmt.order_by(desc(models.Transactions.datetime))
        transactions = db_session.execute(stmt).scalars().all()
        stmt_cat = select(models.Category)
        categories = db_session.execute(stmt_cat).scalars().all()
        cat_map = {c.id: c.name for c in categories}
        for t in transactions:
            t.category_name = cat_map.get(t.category, 'Unknow')
        aggregated_data ={'income': 0, 'spend': 0}
        for t in transactions:
            if t.type == INCOME:
                aggregated_data['income'] += t.amount
            else:
                aggregated_data['spend'] += t.amount

        return render_template('dashboard.html', transactions=transactions, aggregated_data=aggregated_data)
    return redirect('/login')


@app.route('/user/delete', methods=['GET'])
def delete_user():
    return 'delete user'


@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        init_db()
        stmt = select(models.Users).filter_by(email=email, password=password)
        data = db_session.execute(stmt).scalars().first()
        if data:
            session['user_id'] = data.id
            return redirect("/user")
        return redirect("/register")


@app.route('/logout', methods=['GET'])
def log_out():
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        email = request.form['email']
        init_db()
        next_user = models.Users(name=name, surname=surname,
                                 password=password, email=email)
        db_session.add(next_user)
        db_session.commit()
        session['user_id'] = next_user.id
        return redirect('/user')


@app.route('/category', methods=['GET', 'POST'])
def get_all_category():
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            stmt = select(models.Category).filter(or_(models.Category.owner == session['user_id'], models.Category.owner == 1))
            data = db_session.execute(stmt).scalars().all()
            return render_template('user_categories.html', categories=data)
        else:
            category_name = request.form['category_name']
            category_owner = session['user_id']
            new_category = models.Category(name=category_name, owner=category_owner)
            db_session.add(new_category)
            db_session.commit()
            return redirect('/category')
    return redirect('/login')


@app.route('/category/<category_id>', methods=['GET'])
def get_category(category_id):
    if 'user_id' in session:
        init_db()
        stmt = select(models.Category).filter_by(owner_session['user_id'], id= category_id)
        result = db_session.execute(stmt).scalars().first()
    return render_template('single_category.html', one_category=result)


@app.route('/category/<category_id>/edit', methods=['POST'])
def edit_category(category_id):
    if 'user_id' in session:
        category_name = request.form['category_name']
        stmt = select(models.Category).filter_by(owner=session['user_id'], id=category_id)
        result=db_session.execute(stmt).scalas().first()
        db_session.commit()
        return redirect(f'/category/{category_id}')


@app.route('/category/<category_id>/delete', methods=['GET'])
def delete_category(category_id):
    return f'delete category - {category_id}'


@app.route('/income', methods=['GET', 'POST'])
def get_all_income():
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            stmt = (
                select(models.Transactions, models.Category.name.label('category_name'))
                .join(models.Category, models.Transactions.category == models.Category.id)
                .filter(
                    models.Transactions.owner == session['user_id'],
                    models.Transactions.type == INCOME
                )
            )
            result = db_session.execute(stmt).all()

            stmt_cat = select(models.Category).filter(
                or_(models.Category.owner == 1, models.Category.owner == session['user_id'])
            )
            categories = db_session.execute(stmt_cat).scalars().all()

            income_transactions = []
            for transaction, category_name in result:
                income_transactions.append({
                    'id': transaction.id,
                    'description': transaction.description,
                    'category_name': category_name,
                    'amount': transaction.amount,
                    'datetime': transaction.datetime
                })
            return render_template('dashboard_income.html', income_transactions=income_transactions, categories=categories)
        else:
            transaction_description = request.form['description']
            transaction_category = int(request.form['category'])
            transaction_amount = float(request.form['amount'])
            raw_datetime = request.form['datetime']
            transaction_datetime = datetime.strptime(raw_datetime, '%Y-%m-%dT%H:%M')
            transaction_owner = session['user_id']
            transaction_type = INCOME
            new_transaction = models.Transactions(
                description=transaction_description,
                category=transaction_category,
                amount=transaction_amount,
                datetime=transaction_datetime,
                owner=transaction_owner,
                type=transaction_type
            )
            db_session.add(new_transaction)
            db_session.commit()
            return redirect('/income')
    else:
        return redirect('/login')


@app.route('/income/<int:income_id>', methods=['GET'])
def get_income(income_id):
    if 'user_id' in session:
        income = db_session.get(models.Transactions, income_id)
        if income and income.owner == session['user_id']:
            return render_template('income_detail.html', income=income)
    return redirect('/income')



@app.route('/income/<int:income_id>/edit', methods=['GET', 'POST'])
def edit_income(income_id):
    if 'user_id' not in session:
        return redirect('/login')
    income = db_session.get(models.Transactions, income_id)
    if not income or income.owner != session['user_id']:
        return redirect('/income')

    if request.method == 'POST':
        income.description = request.form['description']
        income.amount = float(request.form['amount'])
        income.category = int(request.form['category'])
        income.datetime = datetime.strptime(request.form['datetime'], '%Y-%m-%dT%H:%M')
        db_session.commit()
        return redirect('/income')

    categories = db_session.execute(
        select(models.Category).filter(
            or_(models.Category.owner == 1, models.Category.owner == session['user_id'])
        )
    ).scalars().all()
    return render_template('income_edit.html', income=income, categories=categories)


@app.route('/income/<int:income_id>/delete', methods=['POST'])
def delete_income(income_id):
    if 'user_id' in session:
        income = db_session.get(models.Transactions, income_id)
        if income and income.owner == session['user_id']:
            db_session.delete(income)
            db_session.commit()
        return redirect('/income')
    return redirect('/login')



@app.route('/spend', methods=['GET', 'POST'])
def get_all_spend():
    if 'user_id' in session:
        init_db()
        if request.method == 'GET':
            stmt = (
                select(models.Transactions, models.Category.name.label('category_name'))
                .join(models.Category, models.Transactions.category == models.Category.id)
                .filter(
                    models.Transactions.owner == session['user_id'],
                    models.Transactions.type == SPEND
                )
            )
            result = db_session.execute(stmt).all()

            stmt_cat = select(models.Category).filter(
                or_(models.Category.owner == 1, models.Category.owner == session['user_id'])
            )
            categories = db_session.execute(stmt_cat).scalars().all()

            spend_transactions = []
            for transaction, category_name in result:
                spend_transactions.append({
                    'id': transaction.id,
                    'description': transaction.description,
                    'category_name': category_name,
                    'amount': transaction.amount,
                    'datetime': transaction.datetime
                })
            return render_template('dashboard_spend.html', spend_transactions=spend_transactions, categories=categories)
        else:
            transaction_description = request.form['description']
            transaction_category = int(request.form['category'])
            transaction_amount = float(request.form['amount'])
            raw_datetime = request.form['datetime']
            transaction_datetime = datetime.strptime(raw_datetime, '%Y-%m-%dT%H:%M')
            transaction_owner = session['user_id']
            transaction_type = SPEND
            new_transaction = models.Transactions(
                description=transaction_description,
                category=transaction_category,
                amount=transaction_amount,
                datetime=transaction_datetime,
                owner=transaction_owner,
                type=transaction_type
            )
            db_session.add(new_transaction)
            db_session.commit()
            return redirect('/spend')
    else:
        return redirect('/login')


@app.route('/spend/<int:spend_id>/edit', methods=['GET', 'POST'])
def edit_spend(spend_id):
    if 'user_id' not in session:
        return redirect('/login')
    spend = db_session.get(models.Transactions, spend_id)
    if not spend or spend.owner != session['user_id']:
        return redirect('/spend')

    if request.method == 'POST':
        spend.description = request.form['description']
        spend.amount = float(request.form['amount'])
        spend.category = int(request.form['category'])
        spend.datetime = datetime.strptime(request.form['datetime'], '%Y-%m-%dT%H:%M')
        db_session.commit()
        return redirect('/income')

    categories = db_session.execute(
        select(models.Category).filter(
            or_(models.Category.owner == 1, models.Category.owner == session['user_id'])
        )
    ).scalars().all()
    return render_template('spend_edit.html', spend=spend, categories=categories)


@app.route('/spend/<int:spend_id>/delete', methods=['POST'])
def delete_spend(spend_id):
    if 'user_id' in session:
        spend = db_session.get(models.Transactions, spend_id)
        if spend and spend.owner == session['user_id']:
            db_session.delete(spend)
            db_session.commit()
        return redirect('/spend')
    return redirect('/login')






if __name__ == '__main__':
    app.run()





