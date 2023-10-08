from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

class Recipe(BaseModel):
    id: Optional[str] = Field(None, alias = '_id')
    author: str
    num_liked: int
    name: str
    description: str
    category: str
    details: dict
    nutrition: dict
    ingredients: List[dict]
    directions: List[str]
    imageId: Optional[str]

    def to_json(self):
        return jsonable_encoder(self)

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return data