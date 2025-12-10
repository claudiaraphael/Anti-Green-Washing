from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Pydantic model for User

# Request Schema
# create new user
class UserInputSchema(BaseModel):
    """
    
    Schema para os dados de entrada do usuario (criação/atualização)
    
    """

    username: str = Field(description="Username", example="Cacau")
    
    email: str = Field(description="Email", example="cacau@gmail.com")

# Response Schema
class UserResponseSchema(UserInputSchema):
    """
    Returns user id and date created using name and email from request as input
    """

    id: int = Field(description="Unic user ID", example="123")

    # date_created será retornado como string (formato ISO 8601)
    date_created: str = Field(description="Date of creation")