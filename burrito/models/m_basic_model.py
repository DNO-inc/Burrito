import datetime

from pydantic import BaseModel, Field


class MongoBaseModel(BaseModel):
    class Meta:
        table_name: str = ""


class MongoTTLModel(BaseModel):
    obj_creation_time: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
