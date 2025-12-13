from sqlalchemy.orm import Session
from app.models.categories import CategoriesModel
from app.schemes.categories import CategoryCreate, CategoryUpdate

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(CategoriesModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, category_id: int):
        return self.db.query(CategoriesModel).filter(CategoriesModel.id == category_id).first()
    
    def get_by_name(self, name: str):
        return self.db.query(CategoriesModel).filter(CategoriesModel.name == name).first()
    
    def create(self, category: CategoryCreate):
        db_category = CategoriesModel(
            name=category.name,
            description=category.description
        )
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def update(self, category_id: int, category_update: CategoryUpdate):
        db_category = self.get_by_id(category_id)
        if not db_category:
            return None
        
        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        self.db.commit()
        self.db.refresh(db_category)
        return db_category
    
    def delete(self, category_id: int):
        db_category = self.get_by_id(category_id)
        if not db_category:
            return False
        
        self.db.delete(db_category)
        self.db.commit()
        return True