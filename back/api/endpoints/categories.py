from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dependencies import get_db
from db.repositories.category_repository import category_repository
from schemas.category import CategorySchema, CategoryCreate, CategoryUpdate

router = APIRouter()

@router.get("/", response_model=List[CategorySchema])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all categories with pagination
    """
    return category_repository.get_multi(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get a category by ID
    """
    category = category_repository.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategorySchema)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category
    """
    # Check if category with this name already exists
    existing_category = category_repository.get_by_name(db, name=category_in.name)
    if existing_category:
        return existing_category
    
    return category_repository.create(db, obj_in=category_in)

@router.put("/{category_id}", response_model=CategorySchema)
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    """
    Update a category
    """
    category = category_repository.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category_repository.update(db, db_obj=category, obj_in=category_in)

@router.delete("/{category_id}", response_model=CategorySchema)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category
    """
    category = category_repository.get(db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return category_repository.remove(db, id=category_id)
