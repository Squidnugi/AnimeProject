from flask import Flask, render_template, request, url_for, redirect, make_response
import sqlite3

print("http://localhost:5000/")
app = Flask(__name__)

def get_id_user(type):
    name = request.cookies.get('user')
    with sqlite3.connect('identifier.sqlite') as con:
        cur = con.cursor()

        cur.execute('SELECT username, ID FROM users')

        rows = cur.fetchall()

        for i in rows:
            if i[0] == name:
                users = i[0]
                ID = i[1]
    if type:
        return users
    else:
        return ID

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

            cur2.execute('SELECT * FROM manga_db ORDER BY name ASC')

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

@app.route('/sign_out', methods = ['GET', 'POST'])
def sign_out():
    if request.method == 'POST':
        resp = make_response(redirect(url_for('main')))
        resp.delete_cookie('user')
        return resp
    else:
        return render_template('sign_out.html')

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        img = request.form['img']
        vol = int(request.form['vol'])
        vol_max = request.form['vol_max']
        if vol_max == '':
            vol_max = 0
        else:
            vol_max = int(vol_max)
        if img == '':
            img == 'Blank'
        ID = get_id_user(False)
        with sqlite3.connect("identifier.sqlite") as con:
            cur = con.cursor()

            cur.execute('INSERT INTO manga_db (user_ID, name, volumes, volumes_max, img) VALUES (?, ?, ?, ?, ?)', (ID, name, vol, vol_max, img))
            con.commit()
        print(name, type(name))
        print(img, type(name))
        print(vol, type(vol))
        print(vol_max, type(vol_max))
        return redirect(url_for('main'))
    else:
        return render_template('add.html')

@app.route('/edit/', methods = ['GET', 'POST'])
def edit():
    if request.method == 'POST':
        manga = request.form['manga']
        img = request.form['img']
        vol = int(request.form['vol'])
        vol_max = request.form['vol_max']
        ID = request.form['ID']
        print(vol_max)
        if vol_max == '':
            vol_max = 0
        else:
            vol_max = int(vol_max)
        if img == '':
            img == 'Blank'
        print(manga, vol, vol_max, img, ID)
        print(type(manga), type(vol), type(vol_max), type(img), type(ID))
        with sqlite3.connect("identifier.sqlite") as con:
            cur = con.cursor()

            cur.execute('UPDATE manga_db SET name = ?, volumes = ?, volumes_max = ?, img = ? WHERE ID = ?', (manga, vol, vol_max, img, ID))
            con.commit()
        print(manga, type(manga))
        print(img, type(manga))
        print(vol, type(vol))
        print(vol_max, type(vol_max))
        return redirect(url_for('main'))
    else:
        ID = int(request.args.get('test'))
        print(type(ID))
        values = {}
        with sqlite3.connect('identifier.sqlite') as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM manga_db')

            manga = cur.fetchall()

            for i in manga:
                if i[0] == ID:
                    values['ID'] = i[0]
                    values['user_ID'] = i[1]
                    values['name'] = i[2]
                    values['vol'] = i[3]
                    values['vol_max'] = i[4]
                    values['img'] = i[5]
        print(values)
        return render_template('edit.html', info=values)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        print('test')
        ID = request.form['dele']
        with sqlite3.connect("identifier.sqlite") as con:
            cur = con.cursor()

            cur.execute('DELETE FROM manga_db WHERE ID = ?', (ID,))
            con.commit()
        return redirect(url_for('main'))
    else:
        values = {}
        ID = int(request.args.get('test'))
        with sqlite3.connect("identifier.sqlite") as con:
            cur = con.cursor()

            cur.execute('SELECT * FROM manga_db')
            con.commit()

            manga = cur.fetchall()

            for i in manga:
                if i[0] == ID:
                    values['ID'] = i[0]
                    values['user_ID'] = i[1]
                    values['name'] = i[2]
                    values['vol'] = i[3]
                    values['vol_max'] = i[4]
                    values['img'] = i[5]
        return render_template('delete.html', values=values)

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
