from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Schemas de Entrada (Request Body) ---


class ProductInputSchema(BaseModel):
    """
    Schema para os dados de entrada ao criar um novo produto (POST).
    O nome é opcional pois o sistema pode buscá-lo via barcode.
    """

    # Campo 'name' opcional: se não vier no JSON, o backend busca na Open Food Facts
    name: Optional[str] = Field(
        None,
        json_schema_extra={
            "description": "Nome do produto (opcional se houver barcode).",
            "example": "Sabão Eco Green"
        }
    )

    # Campo 'barcode' continua obrigatório para o scanner funcionar
    barcode: str = Field(
        ...,
        json_schema_extra={
            "description": "Código de barras do produto (EAN-13).",
            "example": "7891234567890"
        }
    )

    user_id: Optional[int] = Field(None, json_schema_extra={"example": 1})


# --- Schemas de Saída (Response Body) ---

class ProductResponseSchema(ProductInputSchema):
    """
    Schema para o retorno completo do Truth Label.
    Inclui os dados processados e as tags de análise.
    """

    id: int = Field(..., json_schema_extra={
                    "description": "ID interno no banco."})

    # URL da imagem para o card do frontend
    image_url: Optional[str] = Field(None, json_schema_extra={
                                     "description": "Link da foto do produto."})

    # Truth Label Score (0 a 100)
    score: Optional[float] = Field(
        None,
        json_schema_extra={"description": "Score de 0 a 100.", "example": 95.6}
    )

    # Nível de processamento (1 a 4)
    nova_group: Optional[int] = Field(None, json_schema_extra={"example": 1})

    # Tags de análise (armazenadas como strings conforme o Model)
    ingredients_analysis_tags: Optional[str] = None
    labels_tags: Optional[str] = None
    allergens_tags: Optional[str] = None
    additives_tags: Optional[str] = None

    date_inserted: datetime = Field(..., json_schema_extra={
                                    "description": "Data do scan."})
