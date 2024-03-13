from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home/index.html')

@app.route("/builder")
def builder():
    return render_template('builder/index.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard/index.html')
