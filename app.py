from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        temp = request.form['temp']
        return render_template('index.html', hello=f'Hi {temp}')
    else:
        return render_template('test.html')


if __name__ == '__main__':
    app.run()
