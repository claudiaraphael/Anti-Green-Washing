from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

# Pydantic model for User

# --- Schemas de Entrada (Request Body) ---

class UserInputSchema(BaseModel):
    """
    Schema para os dados de entrada (criação/atualização) de um usuário. 
    Todos os campos são obrigatórios para a criação de um novo recurso (POST).
    """
    
    # O uso de '...' (Ellipsis) torna o campo obrigatório. 
    # Usamos json_schema_extra para metadados (Swagger/OpenAPI).
    username: str = Field(
        ...,
        json_schema_extra={
            "description": "Nome de usuário único.", 
            "example": "cacau"
        }
    )

    # EmailStr garante que o valor seja um email válido. O campo é obrigatório.
    email: EmailStr = Field(
        ...,
        json_schema_extra={
            "description": "Email único do usuário.", 
            "example": "cacau@gmail.com"
        }
    )


# --- Schemas de Saída (Response Body) ---

class UserResponseSchema(UserInputSchema):
    """
    Schema para o retorno (Response Body) de um usuário.
    Estende UserInputSchema e adiciona campos gerados pelo sistema.
    """
    
    id: int = Field(
        ...,
        json_schema_extra={
            "description": "ID único do usuário no banco de dados.", 
            "example": 1
        }
    )
    
    # Usamos o tipo datetime. O Pydantic V2 o serializa para uma string ISO 8601 no JSON.
    date_created: datetime = Field(
        ...,
        json_schema_extra={
            "description": "Data de criação do usuário (ISO 8601).", 
            "example": "2025-12-10T16:00:00"
        }
    )