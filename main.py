from flask import Flask, render_template,  request, redirect, url_for
from tortoise import fields, models, Tortoise
from tortoise.exceptions import IntegrityError

class User(models.Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=50)
    cash = fields.DecimalField(max_digits=10, decimal_places=2)

async def initalizeDB():
    await Tortoise.init(db_url='sqlite://usersdb.sqlite3', modules={'models': ['__main__']})
    await Tortoise.generate_schemas()

async def create_user(username: str, password: str, cash: float) -> None:
    if isinstance(cash, float):
        user = await User(username=username, password=password, cash=cash)
    else:
        raise ValueError('Please use a decimal num like 1456.44, must be less than 10 digits')
    await user.save()

async def get_user_with_username(username: str):
    user = await User.get(username=username)
    return user

async def deduct_from_bal(username: str, deduct: float) -> None:
    user = await get_user_with_username(username=username)
    user.cash -= deduct
    await user.save()

#warning dev only func follows this line, will delete all users
async def delete_all_users():
    await User.all().delete
#end of the func


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
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
                user = get_user_with_username(username=username)
            except:
                return render_template('index.html', er="<h5>Account does not exist</h5>")
        elif action == 'register':
            return redirect(url_for('register'))
    elif request.method == 'GET':
        return render_template('index.html', er='')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['userr']
        passs = request.form['passs']
        cash = request.form['cash']
        try:
            create_user(username=username,  password=passs, cash=float(cash))
        except ValueError:
            return render_template('register.html', err_msg='<h5 id="oops">Account Creation Failed: try entering a number less than 10 total digits, and up to only 2 decimal places like "13462.33" in the funding field.</h5>')
        except IntegrityError:
            return render_template('register.html', err_msg='<h5 id="oops">The Username is taken.</h5>')
        return f'successfull, user is {username} and pass is **|{passs}|** and money in account is {cash}. Please return to gianbank.tk and login'
    elif request.method == 'GET':
        return render_template('register.html', err_msg='')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    cost = request.args.get('cash')

async def main():
    await initalizeDB()
    app.run()

if __name__ == '__main__':
    import asyncio
    delete_all_users() #delete line if using
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())