from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)
        if not user or not pwd_context.verify(password, user.password):
            return None
        return user
    
    def create_user(self, user_data: UserCreate):
        hashed_password = pwd_context.hash(user_data.password)
        db_user = User(
            username=user_data.username,
            password=hashed_password,
            role=user_data.role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
