from flask import Flask, render_template,  request, redirect, url_for
from tortoise import fields, models, Tortoise

class User(models.Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)
    cash = fields.DecimalField(max_digits=10, decimal_places=2)

async def initalizeDB():
    await Tortoise.init(db_url='sqlite://db.users', modules={'models': ['__main__']})
    await Tortoise.generate_schemas()

async def create_user(username: str, password: str, cash: float) -> None:
    user = User(username=username, password=password, cash=cash)
    await user.save()

async def get_user_with_username(username: str):
    user = await User.get(username=username)
    return user

async def deduct_from_bal(username: str, deduct: float) -> None:
    user = get_user_with_username(username=username)
    user.cash -= deduct
    await user.save()

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
    