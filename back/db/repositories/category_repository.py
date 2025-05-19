from typing import List, Optional
from sqlalchemy.orm import Session

from db.repositories.base import BaseRepository
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate

class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):
    """Repository for category operations"""
    
    def __init__(self):
        super().__init__(Category)
    
    def get_by_name(self, db: Session, *, name: str) -> Optional[Category]:
        """Get a category by name"""
        return db.query(Category).filter(Category.name == name).first()
    
    def get_or_create(self, db: Session, *, name: str) -> Category:
        """Get a category by name or create it if it doesn't exist"""
        db_obj = self.get_by_name(db, name=name)
        if db_obj:
            return db_obj
        
        # Create new category
        db_obj = Category(name=name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multiple_by_names(self, db: Session, *, names: List[str]) -> List[Category]:
        """Get multiple categories by names, creating any that don't exist"""
        result = []
        for name in names:
            category = self.get_or_create(db, name=name)
            result.append(category)
        return result

# Create a singleton instance
category_repository = CategoryRepository()
