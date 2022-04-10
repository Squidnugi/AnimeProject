from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    temp = input(">> ")
    return render_template('index.html', hello=f'Hi {temp}')


if __name__ == '__main__':
    app.run()
