# Flask-OpenAPI

Example of flask request-response validation with [pydantic](https://pydantic-docs.helpmanual.io), and generation of openapi docs using [flask-pydantic-spec](https://github.com/turner-townsend/flask-pydantic-spec).

## Pydantic

### Schema Definition

To do a schema, we import in the `BaseModel`, and type in the field name, followed by their data type. Using the example below.

| code | desc |
|-|-|
| `score_th: float` |  field of float is required |
| `min_height: float = 20` |  field of float is optional, if not present, will use default 20 |
| `min_width: float = Field(..., example=0.3, description="Score")` | `...` means required field, example and description will populate the API docs |
| `maxResults: int = Field(None, example=20, description="Maximum detection result to return")` | `None` means optional, if not present, will take 20 as default. |

```python
from pydantic import BaseModel, Field

class RequestSchema(BaseModel):
    maxResults: int = Field(None, example=20, description="Maximum detection result to return")
    min_height: float = 20
    min_width: float = Field(..., example=0.3, description="Score")
    score_th: float
```

### Contraints

To constraint a field, see their [documentation](https://pydantic-docs.helpmanual.io/usage/types/#constrained-types) for a range of functions.

### Example Schema

We can directly give an example request-response in the BaseModel, using the class Config > schema_extra > "example". This example will populate in the API docs.

```python
class RequestSchema(BaseModel):
    maxResults: int = 20
    min_height: float = 0.03
    min_width: float = 0.03
    score_th: float = 0.3
    nms_iou: float = 0.4
    type: str
    image: str

    class Config:
        schema_extra = {
            "example": {
                "maxResults": 20,
                "min_height": 0.03,
                "min_width": 0.03,
                "score_th": 0.3,
                "nms_iou": 0.4,
                "type": "SAFETY_CONE",
                "image": "base64-encoded-image",
            }
        }
```

### Nested Models

To build a nested model, we will need to create separate models for each nesting. As a standard, we try to add a underscore for all nested schemas with the appropriate names, so that they will appear at the body of the API docs Schema section.

```python
class _normalizedVertices(BaseModel):
    x: float = Field(..., example=5.12, description="X-coordinate")
    y: float = Field(..., example=20.56, description="Y-coordinate")
    width: int = Field(..., example=500, description="width in pixel")
    height: int = Field(..., example=600, description="height in pixel")
    score: confloat(gt=0.0, lt=1.0) = Field(..., example=0.79, description="confidence score")

class ResponseSchema(BaseModel):
    normalizedVertices: List[_normalizedVertices]
```

<p align="center">
    <img src="https://github.com/mapattacker/Flask-OpenAPI/blob/master/apidocs.png?raw=true" width=50% />
</p>


## Validation

If there is a validation error, it will return a specific error message in json.

```python
[
    {
        "ctx": {
            "limit_value": 1.0
        },
        "loc": [
            "nms_iou"
        ],
        "msg": "ensure this value is less than 1.0",
        "type": "value_error.number.not_lt"
    }
]
```

## OpenAPI Docs

Both Swagger-UI & Redocs style documentations will be created automatically, accessible at the endpoints `/apidoc/swagger` and `/apidoc/redoc` respectively.