from sqlalchemy.orm import Session
from app.models.users import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, user_id: int):
        """Находит пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def find_by_username(self, username: str):
        """Находит пользователя по имени"""
        return self.db.query(User).filter(User.username == username).first()
    
    def find_by_email(self, email: str):
        """Находит пользователя по email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def find_all(self):
        """Возвращает всех пользователей"""
        return self.db.query(User).all()
    
    def create(self, user_data):
        """Создает нового пользователя"""
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
    
    def update(self, user_id: int, **kwargs):
        """Обновляет пользователя"""
        user = self.find_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int):
        """Удаляет пользователя"""
        user = self.find_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
