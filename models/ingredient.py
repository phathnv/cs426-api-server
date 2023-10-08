from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

class ListIngredient(BaseModel):
    id: Optional[str] = Field(None, alias = '_id')
    list: List[str]
    
    def to_json(self):
        return jsonable_encoder(self, exclude={'id'})

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return data