import numpy as np
from flask import Flask
from flask import request
from flask import jsonify

import test

app = Flask(__name__)

# method to access the CV2D algorithm as an api (using http requests)
@app.route('/')
def function():
    cord3D = test.main()
    return {"Coordinates" : cord3D.tolist()}


app.run(host="0.0.0.0")