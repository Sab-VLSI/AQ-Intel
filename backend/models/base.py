"""
Base model configurations for MongoDB documents.
Handles Pydantic v2 ObjectId serialization and validation.
"""

from typing import Annotated, Any, Optional
from bson import ObjectId
from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import core_schema

class _ObjectIdPydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: Any) -> ObjectId:
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, str):
                if ObjectId.is_valid(value):
                    return ObjectId(value)
                raise ValueError("Invalid ObjectId format")
            raise ValueError("Type must be ObjectId or valid string")

        return core_schema.no_info_wrap_validator_function(
            validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_dict_handler(
                lambda val: str(val)
            ),
        )

# Pydantic v2 compatible ObjectId representation type
PyObjectId = Annotated[ObjectId, _ObjectIdPydanticAnnotation]

class MongoBaseModel(BaseModel):
    """
    Base model class for all MongoDB collection documents.
    Maps '_id' to 'id' automatically.
    """
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

