"""flask server with pydantic validation & openapi integration"""

from typing import List

from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel, Field, confloat

from predict import prediction

app = Flask(__name__)
api = FlaskPydanticSpec()


class RequestSchema(BaseModel):
    maxResults: int = 20
    min_height: float = 0.3
    min_width: float = 0.3
    score_th: float = 0.3
    nms_iou: float = 0.4
    type: str "safetycone"
    image: str

class _normalizedVertices(BaseModel):
    x: float
    y: float
    width: int
    height: int
    score: confloat(gt=0.0, lt=1.0)

class ResponseSchema(BaseModel):
    normalizedVertices: List[_normalizedVertices]


@app.route("/predict", methods=["POST"])
@api.validate(
    body=Request(RequestSchema),
    resp=Response(HTTP_200=ResponseSchema)
)
def get_predictions():
    JScontent = request.json
    img = JScontent["image"]
    response = prediction(img)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
