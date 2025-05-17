from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from bdd.database import SessionLocal
from bdd.models import User
from auth import verify_password, create_access_token
from typing import Generator, Dict

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", tags=["auth"])
def login(request: LoginRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    try:
        user: User | None = db.query(User).filter(User.username == request.username).first()
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")

        token: str = create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}

    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erreur serveur lors de la connexion")
