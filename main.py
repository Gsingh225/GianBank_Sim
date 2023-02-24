from flask import Flask, render_template,  request

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
            return render_template('register.html')
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run()