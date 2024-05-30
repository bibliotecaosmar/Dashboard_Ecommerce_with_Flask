from flask import render_template
from app import app

@app.route("/<usuario>")
@app.route("/", defaults={"usuario":None})
def index(usuario):
    return render_template('index.html', usuario=usuario)

@app.route("/teste/")
def teste():
    return render_template('base.html')
