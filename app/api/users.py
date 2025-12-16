from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel
from app.schemes.users import UserCreate, UserUpdate, UserResponse
from app.services.users import UserService
from app.api.dependencies import get_user_service
import hashlib
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])
# Login request schema
class LoginRequest(BaseModel):
    username: str
    password: str
    
class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: int = None
    username: str = None
    role: str = None

@router.get("/", response_model=list[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service)
):
    """Get all users with pagination"""
    try:
        return service.get_all_users(skip, limit)
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users"
        )

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Get single user by ID"""
    try:
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user"
        )

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create new user"""
    try:
        user = service.create_user(user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    """Update existing user"""
    try:
        user = service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Delete user"""
    try:
        if not service.delete_user(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )

@router.post("/login", response_model=LoginResponse)
def login_user(
    login_data: LoginRequest,
    service: UserService = Depends(get_user_service)
):
    """Authenticate user and return user data"""
    try:
        logger.info(f"Login attempt for user: {login_data.username}")
        
        user = service.authenticate(login_data.username, login_data.password)
        if not user:
            logger.warning(f"Failed login for user: {login_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        logger.info(f"Successful login for user: {login_data.username}")
        return LoginResponse(
            success=True,
            message="Login successful",
            user_id=user.id,
            username=user.username,
            role=getattr(user, 'role', 'user')
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during authentication"
        )
