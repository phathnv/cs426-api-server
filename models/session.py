from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.encoders import jsonable_encoder

class Session(BaseModel):
    id: Optional[str] = Field(None, alias = '_id')
    token: str
    user_id: str 
    exp_time: datetime

    def to_json(self):
        return jsonable_encoder(self)

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return data
    