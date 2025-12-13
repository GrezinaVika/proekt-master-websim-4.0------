from sqlalchemy.orm import Session
from app.models.roles import Role
from app.schemes.roles import RoleCreate, RoleUpdate

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Role).offset(skip).limit(limit).all()
    
    def get_by_id(self, role_id: int):
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_by_name(self, name: str):
        return self.db.query(Role).filter(Role.name == name).first()
    
    def create(self, role: RoleCreate):
        db_role = Role(
            name=role.name,
            description=role.description
        )
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
    
    def update(self, role_id: int, role_update: RoleUpdate):
        db_role = self.get_by_id(role_id)
        if not db_role:
            return None
        
        update_data = role_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_role, field, value)
        
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
    
    def delete(self, role_id: int):
        db_role = self.get_by_id(role_id)
        if not db_role:
            return False
        
        self.db.delete(db_role)
        self.db.commit()
        return True