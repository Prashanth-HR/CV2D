import numpy as np
from flask import Flask
from flask import request
from flask import jsonify

import test

app = Flask(__name__)

@app.route('/')
def function():
    cord3D = np.array(test.main())
    print(cord3D.shape)
    # return jsonify([json(cord) for cord in cord3D])
    return {"cords" : cord3D.reshape(3,3).tolist()}


app.run(host="0.0.0.0")