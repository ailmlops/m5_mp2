from typing import Any, List, Optional
import datetime

from pydantic import BaseModel
from sentiment_model.processing.validation import DataInputSchema


class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    #predictions: Optional[List[int]]
    predictions: Optional[int]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                "ProductId": "B001E4KFG0", 
                "Sentiment": "positive", 
                "UserId": "A3SGXH7AUHU8GW",
                "ProfileName": "delmartian", 
                "Score": 5,
                "Time": "2011-04-27", # datetime.datetime.strptime("2012-11-05", "%Y-%m-%d"),
                "Summary": "Good Quality Dog Food",
                "Text": "I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product better than most.",
                    }
                ]
            }
        }
