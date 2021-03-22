"""flask server with openapi.yml integration"""

import connexion
from flask import request

from predict import prediction

app = connexion.App(__name__, specification_dir='.')


@app.route("/predict", methods=["POST"])
def predict():
    JScontent = request.json
    img = JScontent["image"]
    response = prediction(img)
    return response


if __name__ == "__main__":
    app.add_api('openapi.yml')
    app.run(host="0.0.0.0")