import json
import logging
import os
from pydantic import BaseModel, constr, Field
from typing import Optional
from fastapi import APIRouter

from starlette.responses import JSONResponse

logging.basicConfig(
    format=(
        "%(asctime)s, %(levelname)-8s"
        "[%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s"
    ),
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

router = APIRouter()

from src.modelling import ChatClassifier


classifier = ChatClassifier(
    model_path=os.path.join("data", "logistic_reg_model.joblib"),
    vectorizer_path=os.path.join("data", "vectorizer.pickle"),
)


class RequestMessage(BaseModel):
    text: Optional[str] = Field(None, min_length=5, max_length=1000)


class Response(BaseModel):
    label: str
    probability: float


@router.post("/predict_message_type")
def predict_message(parameters: RequestMessage) -> Response:
    """Predict type of message from chat

    Args:
        parameters (RequestMessage): text of message

    Returns:
        Response: model prediction result and probability of class
    """
    result = classifier.predict(
        text=parameters.text,
    )

    human_name = {0: "Python chat 🐍", 1: "DS chat👾"}

    responce = Response(
        **{"label": human_name[result["label"]], "probability": result["probability"]}
    )
    return responce
