from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    """Base schema for category data"""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Schema for creating a new category"""
    pass

class CategoryUpdate(CategoryBase):
    """Schema for updating an existing category"""
    name: Optional[str] = None
    description: Optional[str] = None

class CategorySchema(CategoryBase):
    """Schema for category response"""
    id: int
    
    class Config:
        orm_mode = True
