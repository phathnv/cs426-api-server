from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder

class Asset(BaseModel):
    id: str = Field(None, alias = '_id')
    data: bytes

    #def to_json(self):
    #    return jsonable_encoder(self)

    def to_dict(self):
        data = self.model_dump(by_alias=True)
        return data