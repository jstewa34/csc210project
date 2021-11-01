from flask import Flask
from flask import render_template
import os
import json
app = Flask(__name__)

@app.route('/')
def hello(uid=None):
	return render_template('index.html')