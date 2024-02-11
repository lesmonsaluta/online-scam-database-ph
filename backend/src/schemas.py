from pydantic import BaseModel
from typing import Optional, Any, Dict

class InternalErrorResponseSchema(BaseModel):
    error: str
    status_code: int

class ResponseDataSchema(BaseModel):
    numbers: Optional[Any]
    text: Optional[str]

class ImageUploadResponseSchema(BaseModel):
    data: Optional[ResponseDataSchema]
    error: Optional[str]
    success: bool

class ExternalResponseSchema(BaseModel):
    results: Any
    error : Optional[str]
    success : bool
