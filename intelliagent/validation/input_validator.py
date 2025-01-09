from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


class UserInput(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=100)
    input_data: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    context: Optional[Dict[str, Any]] = None

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v.strip():
            raise ValueError("user_id cannot be empty")
        return v.strip()

    @validator('input_data')
    def validate_input_data(cls, v):
        if not v.strip():
            raise ValueError("input_data cannot be empty")
        return v.strip()


class ModelConfig(BaseModel):
    api_key: str = Field(..., min_length=1)
    model: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=150, gt=0)
    domain: str = Field(default="general")
    continuous_learning: bool = Field(default=True)

    @validator('api_key')
    def validate_api_key(cls, v):
        if not v.strip():
            raise ValueError("api_key cannot be empty")
        return v.strip()

    @validator('model')
    def validate_model(cls, v):
        allowed_models = ["gpt-4", "gpt-3.5-turbo"]
        if v not in allowed_models:
            raise ValueError(f"model must be one of {allowed_models}")
        return v
