from flask import Flask, render_template,  request, redirect, url_for
from tortoise import fields, models, Tortoise

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['user']
        pas = request.form['pas']
        action = request.form['action']
        #return f'user name is {username}, password is {pas}  and action requested is {action}'
        if action == 'login':
            return render_template('acc.html')
        elif action == 'register':
            return redirect(url_for('register'))
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['userr']
        passs = request.form['passs']
        cash = request.form['cash']
        return 'hi'
    elif request.method == 'GET':
        return render_template('register.html')

if __name__ == '__main__':
    app.run()
    