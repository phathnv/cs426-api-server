from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

class Category(BaseModel):
    id: str = Field(None, alias = '_id')
    name: str
    imageid: str
    recipes: List[str]

    def to_json(self):
        return jsonable_encoder(self)

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return data