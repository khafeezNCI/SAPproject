from flask import Flask, render_template, request, session, flash, g
from datetime import datetime
import logging
import user


app = Flask(__name__)
app.secret_key = "very secret key"

logging.basicConfig(filename='monitor.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')


@app.route('/set_up', methods=["GET", "POST"])
def set_up():
    user.create_table_user()
    user.insert_default_users()
    app.logger.info('Info tabase created')
    return render_template('index.html', utc_dt=datetime.utcnow(), isIndex=False)


@app.route('/', methods=["GET", "POST"])
def index():
    if 'logged_in' not in session:
        session['logged_in'] = False

    return render_template('index.html', utc_dt=datetime.utcnow(), isIndex=session['logged_in'])


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if request.method == 'GET':
        print("go to login form")
        print(session['logged_in'])
        return render_template('login.html', isIndex=session['logged_in'])
    else:
        data = user.get_user_email(request.form['username'])
        print(data)
        print(data[0][1])
        print(data[0][2])
        print(data[0][3])
        if request.form['username'] == data[0][2] and request.form['password'] == data[0][3]:
            session['logged_in'] = True
            print(session['logged_in'])
            return index()
        else:
            flash('wrong password!')
            session['logged_in'] = False
            return index()


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        print("go to login form")
        print(session['logged_in'])
        return render_template('user.html', isIndex=session['logged_in'])
    else:
        print(request.form['username'])
        data = user.get_user_name(request.form['username'])
        print(data)
        return render_template('user.html', isIndex=session['logged_in'], data=data)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POSt'])
def register():
    if request.method == 'GET':
        print("go to register form")
        return render_template('register.html')
    else:
        print(request.form['username'])
        print(request.form['password'])
        return render_template('login.html')


@app.route("/xss", methods=['GET', 'POSt'])
def xss():
    if request.method == 'GET':
        data = request.args.get('name')
        print("go to xss example")
        return render_template('xss.html', data=data)
    else:
        print(request.form['xssname'])
        return render_template('xss.html', data=request.form['xssname'])

# add error handler to provide better feebask to the user


@app.errorhandler(404)
def page_not_found(e):
    logging.error("404 error Page not found")
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    logging.error("500 error internal server")
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
