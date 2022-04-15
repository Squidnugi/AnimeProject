from flask import Flask, render_template, request, url_for, redirect, make_response
import sqlite3

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def main():
    users = ''
    ID = 0
    values = []
    name = request.cookies.get('user')
    with sqlite3.connect('identifier.sqlite') as con:
        cur = con.cursor()

        cur.execute('SELECT username, ID FROM users')

        rows = cur.fetchall()

        for i in rows:
            if i[0] == name:
                users = i[0]
                ID = i[1]
    if name == users:
        with sqlite3.connect('identifier.sqlite') as con:
            cur2 = con.cursor()

            cur2.execute('SELECT * FROM manga_db')

            manga = cur2.fetchall()

            for i in manga:
                if i[1] == ID:
                    temp = {}
                    temp['ID'] = i[0]
                    temp['user_ID'] = i[1]
                    temp['name'] = i[2]
                    temp['vol'] = i[3]
                    temp['vol_max'] = i[4]
                    temp['img'] = i[5]
                    values.append(temp)
        return render_template('index.html', name=name, table=values)
    else:
        return render_template('welcome.html')

@app.route('/sign_up', methods = ['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        temp = []
        user = request.form['username']
        temp.append(user)
        password = request.form['password']
        temp.append(password)
        with sqlite3.connect("identifier.sqlite") as con:
            cur = con.cursor()
            print('sup')
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", temp)
            con.commit()
        resp = make_response(redirect(url_for('main')))
        resp.set_cookie('user', user)
        return resp
    else:
        return render_template('sign_up.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        logged = False
        user = request.form['username']
        password = request.form['password']
        print('hi')
        with sqlite3.connect("identifier.sqlite") as con:
            cur = con.cursor()

            cur.execute('SELECT username, password FROM users')

            rows = cur.fetchall()

            for i in rows:
                if i[0] == user:
                    if i[1] == password:
                        logged = True
        if logged:
            resp = make_response(redirect(url_for('main')))
            resp.set_cookie('user', user)
            return resp
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run()
