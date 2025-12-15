from sqlalchemy.orm import Session
from app.models.users import User

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data):
        db_user = User(
            username=getattr(user_data, 'username', 'user'),
            email=getattr(user_data, 'email', 'user@example.com'),
            hashed_password=getattr(user_data, 'hashed_password', 'password'),
            full_name=getattr(user_data, 'full_name', ''),
            is_active=True,
            is_superuser=False
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_data):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for key, value in vars(user_data).items():
            if not key.startswith('_') and hasattr(user, key):
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
