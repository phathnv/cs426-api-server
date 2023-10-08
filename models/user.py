from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

class User(BaseModel):
    id: str = Field(None, alias = '_id')
    token: Optional[str] = Field(None, alias = '_token')
    pwd: str = Field(None, alias = '_pwd')
    code: Optional[str] = Field(None, alias = '_code')
    code_exp: Optional[datetime] = Field(None, alias= "_code_exp")
    email: str
    avatar: Optional[str] = None
    username: Optional[str] = None
    dob: Optional[datetime] = None
    country: Optional[str] = None
    posts: List[str]
    likes: List[str]
    created_at: datetime

    def to_json(self):
        return jsonable_encoder(self, exclude={'pwd', 'token', 'code', 'code_exp'})

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return data