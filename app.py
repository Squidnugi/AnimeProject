from flask import Flask, render_template, request, url_for, redirect, make_response

app = Flask(__name__)
users = ['Squid']

@app.route('/', methods = ['POST', 'GET'])
def main():
    name = request.cookies.get('user')
    if name in users:
        return render_template('index.html', name=name)
    else:
        return render_template('welcome.html')

@app.route('/sign_up', methods = ['POST', 'GET'])
def sign_up():
    return render_template('sign_up.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        resp = make_response(redirect(url_for(main)))
        resp.set_cookie('user', user)
        return resp
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run()
