from pydantic import BaseModel


class MongoBaseModel(BaseModel):
    class Meta:
        table_name: str = ""
