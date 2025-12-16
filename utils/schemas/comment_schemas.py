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

    """
    O que são schemas

    É uma padronização dos formatos de entrada e saída de dados da API.
    Garante que os dados tenham o tipo correto e que fornecam os campos esperados.
    
    Se um cliente envia um "Produto", o Schema de Produto garante que ele tenha o name e o barcode e que eles sejam strings. 
    Se a API retorna um "Comentário", o Schema de Comentário garante que ele inclua o id e a date_inserted.
    
    É responsável pelo controle de qualidade dos dados antes de eles chegarem ao banco de dados SQLite da API.

    Exemplos Práticos no Seu Código:

    Obrigatório? No UserInputSchema, o uso de ... (Ellipsis) garante que o campo username não pode ser vazio. Se o cliente não enviar, ele é rejeitado.

    Formato de Email? O tipo EmailStr verifica se o que foi enviado no campo email é, de fato, um email válido (ex: a@b.com é aceito, ab.com é rejeitado).

    Limites? No CommentInputSchema, ele garante que o n_estrela (nota) seja um número entre 0 e 5, rejeitando notas como 10 ou -1.

    ERRO 422 - VALIDAÇÃO DE DADOS FALHOU

    Se a validação falha, a API nem tenta salvar no banco. Ela responde imediatamente com um erro (código 422), economizando tempo e protegendo o seu sistema.


    pydantic faz a serialização dos dados, ou seja, traduz os dados recebidos para um formato legível pela internet (JSON), como o datetime por exemplo que vira uma string "2025-12-10T16:00:00".

    """
