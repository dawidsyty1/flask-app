"""DataUsage schemas to assist with sub serialization"""
from enum import Enum
from marshmallow import fields, Schema
from marshmallow_enum import EnumField


class StatusDataUsagesAmong(Enum):
    succeed = "succeed"
    error = "error"


class DataUsagesAmongSchema(Schema):
    """Schema class to handle serialization of among data usage """
    gb_used = fields.Float()
    status = EnumField(StatusDataUsagesAmong)
