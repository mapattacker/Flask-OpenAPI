"""flask server with pydantic validation & openapi integration"""

from typing import List

from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec, Request, Response
from pydantic import BaseModel, Field, confloat

from predict import prediction

app = Flask(__name__)
api = FlaskPydanticSpec("flask", title="Objection Detection", version="v1.0.0")


class RequestSchema(BaseModel):
    maxResults: int = Field(None, example=20, description="Maximum detection result to return")
    min_height: float = Field(None, example=0.3, description="Score")
    min_width: float = Field(None, example=0.3, description="Score")
    score_th: float = Field(None, example=0.3, description="Score")
    nms_iou: float = Field(..., example=0.4, description="Non-max suppression, intersection over union")
    type: str = Field(..., example="safetycone", description="name of object to detect")
    image: str = Field(..., description="base64-encoded-image")

class _normalizedVertices(BaseModel):
    x: float = Field(..., example=5.12, description="X-coordinate")
    y: float = Field(..., example=20.56, description="Y-coordinate")
    width: int = Field(..., example=500, description="width in pixel")
    height: int = Field(..., example=600, description="height in pixel")
    score: confloat(gt=0.0, lt=1.0) = Field(..., example=0.79, description="confidence score")

class ResponseSchema(BaseModel):
    normalizedVertices: List[_normalizedVertices]


@app.route("/predict", methods=["POST"])
@api.validate(
    body=Request(RequestSchema),
    resp=Response(HTTP_200=ResponseSchema),
    tags=["API Name"]
)
def get_predictions():
    """Short description of endpoint

    Long description of endpoint"""
    JScontent = request.json
    img = JScontent["image"]
    response = prediction(img)
    return response


if __name__ == "__main__":
    api.register(app)
    app.run(host="0.0.0.0")