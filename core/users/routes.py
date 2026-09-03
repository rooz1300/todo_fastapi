from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from users.models import UserModel
from users.schemas import UserLoginSchema, UserCreateSchema, UserReturnSchema

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user.
    """
    # 1. Find user by username
    user = db.query(UserModel).filter(UserModel.username == request.username).first()
    
    # 2. Verify user exists and password matches
    if not user or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Inactive user"
        )

    return {"message": "Login successful", "user_id": user.id}

@router.post("/register", response_model=UserReturnSchema, status_code=status.HTTP_201_CREATED)
async def register_user(request: UserCreateSchema, db: Session = Depends(get_db)):
    # 1. Check if username already exists
    existing_user = db.query(UserModel).filter(UserModel.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )

    # 2. Create new user instance
    new_user = UserModel(username=request.username)
    
    # 3. Hash the password using the model method
    new_user.hash_password(request.password)

    # 4. Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user