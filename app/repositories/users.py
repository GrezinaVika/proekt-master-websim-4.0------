from sqlalchemy.orm import Session
from app.models.users import User
from app.schemes.users import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: UserCreate):
        # В реальном приложении здесь нужно хэшировать пароль
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.password,  # Внимание: нужно хэшировать!
            full_name=user.full_name
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, user_update: UserUpdate):
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password" and value:
                # Хэшировать пароль при обновлении
                db_user.hashed_password = value  # Внимание: нужно хэшировать!
            else:
                setattr(db_user, field, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int):
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def authenticate(self, username: str, password: str):
        user = self.get_by_username(username)
        if not user:
            return None
        
        # В реальном приложении проверять хэшированный пароль
        if user.hashed_password == password:  # Внимание: использовать хэширование!
            return user
        return None