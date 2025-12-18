from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# --- Input Schemas (Request Body) ---


class ProductInputSchema(BaseModel):
    name: Optional[str] = Field(
        None,
        description="Product name (optional if barcode is provided).",
        # Backwards compatible way
        json_schema_extra={"example": "Eco Green Soap"}
    )

    barcode: str = Field(
        ...,
        description="Product barcode (EAN-13).",
        json_schema_extra={"example": "7891234567890"},
    )

    user_id: Optional[int] = Field(None, json_schema_extra={"example": 1})

# --- Output Schemas (Response Body) ---


class ProductResponseSchema(ProductInputSchema):
    """
    Schema for the complete Truth Label response.
    Includes processed data and analysis tags.
    """

    id: int = Field(..., json_schema_extra={
                    "description": "Internal database ID."})

    # Image URL for the frontend card
    image_url: Optional[str] = Field(None, json_schema_extra={
                                     "description": "Product image link."})

    # Truth Label Score (0 to 100)
    score: Optional[float] = Field(
        None,
        json_schema_extra={
            "description": "Sustainability/Health score from 0 to 100.", "example": 95.6}
    )

    # Industrial processing level (1 to 4)
    nova_group: Optional[int] = Field(None, json_schema_extra={"example": 1})

    # Analysis tags (stored as strings to be compatible with SQLite)
    ingredients_analysis_tags: Optional[str] = None
    labels_tags: Optional[str] = None
    allergens_tags: Optional[str] = None
    additives_tags: Optional[str] = None

    date_inserted: datetime = Field(..., json_schema_extra={
                                    "description": "Scan timestamp."})
