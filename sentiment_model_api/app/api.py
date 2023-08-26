import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sentiment_model import __version__ as model_version
from sentiment_model.predict import make_prediction

from sentiment_model import __version__ as _version
from sentiment_model.config.core import config
from sentiment_model.processing.data_manager import load_model, load_tokenizer

from tensorflow.keras.preprocessing.sequence import pad_sequences

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()


@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleDataInputs) -> Any:
    """
    sentiment classification model
    """

    #input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))
    
    tokenizer_file_name = f"{config.app_config.tokenizer_save_file}{_version}.json"
    tokenizer = load_tokenizer(file_name = tokenizer_file_name)
    
    text = 'I watched the movie till end'   
    text = tokenizer.texts_to_sequences([text])
    
    #text = tokenizer.texts_to_sequences([input_data.inputs])
    text_pad = pad_sequences(text, 
                             maxlen = config.model_config.max_review_length, 
                             padding= config.model_config.padding_type, 
                             truncating= config.model_config.truncating_type)
    
    results = make_prediction(input_data = text_pad)
    
    #results = make_prediction(input_data=input_df.replace({np.nan: None}))

    # if results["errors"] is not None:
    #     raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    
    return {"predictions":results["predictions"][0]}
