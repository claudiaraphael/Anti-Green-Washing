from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Schemas de Entrada (Request Body) ---

class ProductInputSchema(BaseModel):
    """
    Schema para os dados de entrada ao criar um novo produto (POST).
    Necessita de nome e código de barras para ser cadastrado.
    """
    
    # Campo 'name' é obrigatório.
    name: str = Field(
        ...,
        json_schema_extra={
            "description": "Nome do produto.", 
            "example": "Biscoito Integral Vitao"
        }
    )
    
    # Campo 'barcode' é obrigatório.
    # Usamos 'str' pois códigos de barras longos (EAN-13) são melhor tratados como strings.
    barcode: str = Field(
        ...,
        json_schema_extra={
            "description": "Código de barras do produto (ex: EAN-13).", 
            "example": "7891234567890"
        }
    )
    
    # Adicionando um campo opcional para o ID do usuário que inseriu.
    # Será útil para a lógica de 'deletar produtos' na base de dados local.
    user_id: Optional[int] = Field(
        None,
        json_schema_extra={
            "description": "ID do usuário que cadastrou o produto (opcional).", 
            "example": 1
        }
    )


# --- Schemas de Saída (Response Body) ---

class ProductResponseSchema(ProductInputSchema):
    """
    Schema para o retorno (Response Body) de um produto.
    Inclui campos gerados pelo sistema.
    """
    
    id: int = Field(
        ...,
        json_schema_extra={
            "description": "ID único do produto no banco de dados.", 
            "example": 101
        }
    )
    
    # O Pydantic V2 usará o objeto float nativo. Optional é importante aqui, 
    # pois o eco_score pode ser calculado APÓS a inserção inicial.
    eco_score: Optional[float] = Field(
        None,
        json_schema_extra={
            "description": "Score de sustentabilidade calculado (0 a 5).", 
            "example": 4.5
        }
    )
    
    # Usamos o tipo datetime. O Pydantic V2 o serializa para uma string ISO 8601 no JSON.
    date_inserted: datetime = Field(
        ...,
        json_schema_extra={
            "description": "Data de cadastro do produto (ISO 8601).", 
            "example": "2025-12-10T16:15:00"
        }
    )