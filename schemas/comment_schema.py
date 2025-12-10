from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime

# --- Schemas de Entrada (Request Body) ---

class CommentInputSchema(BaseModel):
    """
    Schema para os dados de entrada ao criar um novo comentário (POST).
    """
    
    # Campo 'product_id' é obrigatório, pois o comentário deve estar atrelado a um produto.
    product_id: int = Field(
        ...,
        json_schema_extra={
            "description": "ID do produto ao qual o comentário se refere.", 
            "example": 101
        }
    )

    # 'text' é o conteúdo do comentário e é obrigatório.
    text: str = Field(
        ...,
        json_schema_extra={
            "description": "Conteúdo do comentário (máx. 500 caracteres).", 
            "example": "O rótulo deste produto é bem claro sobre a origem dos ingredientes."
        }
    )
    
    # conint restringe o valor inteiro para um intervalo (de 0 a 5 estrelas).
    n_estrela: Annotated[
        int,
        Field(
            ge=0,
            le=5,
            json_schema_extra={
                "description": "Nota de 0 a 5 estrelas dada pelo usuário",
                "example": 4
            }
        )
    ]
    
    # Opcionais (Se o usuário estiver logado, passamos o user_id. Senão, podemos usar um nome genérico 'author'.)
    user_id: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "description": "ID do usuário que fez o comentário (opcional, se logado).", 
            "example": 1
        }
    )
    
    author_name: Optional[str] = Field(
        None,
        json_schema_extra={
            "description": "Nome do autor (para comentários não autenticados).", 
            "example": "Visitante Anônimo"
        }
    )


# --- Schemas de Saída (Response Body) ---

class CommentResponseSchema(CommentInputSchema):
    """
    Schema para o retorno (Response Body) de um comentário.
    Inclui campos gerados pelo sistema.
    """
    
    id: int = Field(
        ...,
        json_schema_extra={
            "description": "ID único do comentário no banco de dados.", 
            "example": 501
        }
    )
    
    # O Pydantic V2 serializa o objeto datetime para uma string ISO 8601.
    date_inserted: datetime = Field(
        ...,
        json_schema_extra={
            "description": "Data de inserção do comentário (ISO 8601).", 
            "example": "2025-12-10T16:30:00"
        }
    )