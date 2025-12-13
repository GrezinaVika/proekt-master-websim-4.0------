from sqlalchemy.orm import Session
from app.models.admin import AdminModel
from app.schemes.admin import AdminCreate, AdminUpdate

class AdminRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(AdminModel).offset(skip).limit(limit).all()
    
    def get_by_id(self, admin_id: int):
        return self.db.query(AdminModel).filter(AdminModel.id == admin_id).first()
    
    def get_by_login(self, login: str):
        return self.db.query(AdminModel).filter(AdminModel.login == login).first()
    
    def create(self, admin: AdminCreate):
        db_admin = AdminModel(
            login=admin.login,
            password=admin.password,
            role=admin.role
        )
        self.db.add(db_admin)
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin
    
    def update(self, admin_id: int, admin_update: AdminUpdate):
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return None
        
        update_data = admin_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_admin, field, value)
        
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin
    
    def delete(self, admin_id: int):
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return False
        
        self.db.delete(db_admin)
        self.db.commit()
        return True
    
    def update_last_login(self, admin_id: int):
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return None
        
        from datetime import datetime
        db_admin.last_login = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin