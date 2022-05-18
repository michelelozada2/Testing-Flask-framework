from flask import Flask, render_template
app = Flask('Hello')
@app.route('/')
@app.route('/hello')
def hello():
    return render_template('hello.html')  # pegar o que está em hello.html

@app.route('/tchau')
def tchau():
    return 'Tchau' 