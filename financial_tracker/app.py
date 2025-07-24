from flask import Flask, request, render_template

app = Flask(__name__)

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
        return f'hello world POST {username} {password}'



@app.route('/register', methods=['GET', 'POST'])
def get_register():
    if request.method=='GET':
        return render_template('/register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        return f'hello world POST {username} {password}'


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


