
from burrito.models.m_basic_model import MongoBaseModel, MongoTTLModel


class AccessRenewMetaData(MongoBaseModel, MongoTTLModel):
    user_id: int
    reset_token: str

    class Meta:
        table_name: str = "password_reset_metadata"
