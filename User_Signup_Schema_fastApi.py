from uuid import UUID
from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field, field_validator
import re

app = FastAPI()

# A robust Pydantic data schema for incoming requests
class UserSignupSchema(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, v):
            raise ValueError("value is not a valid email address")
        return v
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    age: int | None = Field(default=None, ge=18, le=120)

@app.post("/users/{organization_id}/register")
async def register_user(
    # 1. Path parameter (explicitly constrained via Path)
    organization_id: Annotated[UUID, Path(description="The unique organization ID ID")],
    
    # 2. Query parameter (inferred because it's a primitive type NOT in the path URL)
    send_welcome_email: Annotated[bool, Query(description="Trigger background welcome email")] = True,
    
    # 3. Request Body (inferred because it's a Pydantic model)
    payload: UserSignupSchema = Body(...)
):
    """
    Deep dive mechanics:
    - organization_id must be a valid UUID format string, or a 422 error triggers.
    - send_welcome_email converts values like 'true', '1', 'on', 'yes' automatically to True.
    - payload parses raw JSON out of the request body and enforces all Field constraints.
    """
    return {
        "org": organization_id,
        "email_sent": send_welcome_email,
        "user": payload.model_dump(exclude={"password"}) # Serialization filter
    }