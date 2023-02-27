from flask import Flask, render_template,  request, redirect, url_for
from tortoise import fields, models, Tortoise
from tortoise.exceptions import IntegrityError
from tortoise.models import Model
import random

class User(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)
    cash = fields.DecimalField(max_digits=10, decimal_places=2)
    tradecash = fields.DecimalField(max_digits=10, decimal_places=2)
    giancard = fields.IntField(unique=True)
    def __str__(self) -> str:
        return self.name
    class  Meta:
        table:  str = 'users'

async def initalizeDB():
    await Tortoise.init(db_url='sqlite://usersdb.sqlite3', modules={'models': ['__main__']})
    await Tortoise.generate_schemas()

async def create_user(username: str, password: str, cash: float) -> None:
    if isinstance(cash, float):
        success = False
        while success != True:
            try:
                card = random.randint(1000000000, 9999999999)
                user = await User(username=username, password=password, cash=cash, tradecash=0.00, giancard=card)
                success = True
            except:
                None
    else:
        raise ValueError('Please use a decimal num like 1456.44, must be less than 10 digits')
    await user.save()

async def get_user_with_username(username: str):
    user = await User.get(username=username)
    return user


async def get_user(username: str) -> tuple[str: float]:
    user = await User.get(username=username)
    password = user.password
    cash = user.cash
    return password, cash

async def deduct_from_bal(username: str, deduct: float) -> None:
    user = await get_user_with_username(username=username)
    user.cash -= deduct
    await user.save()

#warning dev only func follows this line, will delete all users
async def delete_all_users():
    await User.all().delete()

async def get_all() -> None:
    users = await User.all()
    for user in users:
        print(user)
#end of the func


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        username = request.form['user']
        pas = request.form['pas']
        action = request.form['action']
        """
        try:
            user = get_user_with_username(username=username)
        except:
            return render_template('index.html', er="<h5>Account does not exist</h5>")
        #return f'user name is {username}, password is {pas}  and action requested is {action}'
        """
        if action == 'login':
            try:
                user1 = await get_user_with_username(username=username)
                temp1 = user1.username
                temp2 = user1.cash
                temp3 = user1.tradecash
                temp4 = user1.giancard
                return redirect(url_for('dashboard', username=temp1, cash=temp2, tradecash=temp3, giancard=temp4))
            except Exception as e:
                get_all()
                print(e)
                return render_template('index.html', er=f"<h5>Account does not exist  {e}</h5>")
        elif action == 'register':
            return redirect(url_for('register'))
    elif request.method == 'GET':
        return render_template('index.html', er='')

@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        username = request.form['userr']
        passs = request.form['passs']
        cash = request.form['cash']
        try:
            await create_user(username=username,  password=passs, cash=float(cash))
        except ValueError:
            return render_template('register.html', err_msg='<h5 id="oops">Account Creation Failed: try entering a number less than 10 total digits, and up to only 2 decimal places like "13462.33" in the funding field.</h5>')
        except IntegrityError:
            return render_template('register.html', err_msg='<h5 id="oops">The Username is taken.</h5>')
        return f'successfull, user is {username} and pass is **|{passs}|** and money in account is {cash}. Please return to gianbank.tk and login'
    elif request.method == 'GET':
        return render_template('register.html', err_msg='')

@app.route('/dashboard', methods=['POST', 'GET'])
async def dashboard():
    username = request.args.get('username')
    cash = request.args.get('cash')
    tradecash = request.args.get('tradecash')
    giancard = request.args.get('giancard')
    if request.method == 'GET':
        #return f'User is {username} and cash on hand is {cash}'
        return render_template('acc.html', user=username, cash=cash, tradecash=tradecash, giancard=giancard)
    elif request.method == 'POST':
        return redirect(url_for('index'))

async def main():
    await initalizeDB()
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    import asyncio
    delete_all_users() #delete line if using
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
