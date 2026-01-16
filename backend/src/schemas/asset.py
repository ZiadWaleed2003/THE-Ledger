from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# a base schema
class AssetBase(BaseModel):

    name: str = Field(... , description="Name of the asset", example="Ounce of Gold")
    category: str = Field(..., description="Category like Electronics, Furniture", example="Electronics")
    value: float = Field(..., gt=0, description="Monetary value", example=2500.0)
    quantity : float = Field(..., description="quantity of that asset" ,example=2.5)
    status: str = Field(..., description="Current status (e.g., Active, Retired)", example="Active")
    purchase_date: Optional[datetime] = Field(None, description="Date of purchase")


# schema for creating an asset [Post request]
class AssetCreate(AssetBase):
    pass


# Schema for update an asset [Put]
class AssetUpdate(AssetBase):
    name: Optional[str] = None
    category: Optional[str] = None
    value: Optional[float] = None
    quantity: Optional[float] = None
    status: Optional[str] = None
    purchase_date: Optional[datetime] = None

# schema for GET the request
class AssetResponse(AssetBase):
    id: str

    class Config:
        from_attributes = True






