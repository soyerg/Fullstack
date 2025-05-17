from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from bdd.database import SessionLocal
from bdd.models import School
from dependencies import get_current_user
from typing import Optional, Generator, List, Dict
from schemas import SchoolOut  # ✅ Import du schéma

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/schools", tags=["schools"], response_model=List[SchoolOut])
def get_all_schools(db: Session = Depends(get_db)):
    return db.query(School).all()

@router.get("/schools/ips", tags=["schools"], response_model=List[SchoolOut])
def get_schools_by_ips(
    min_ips: Optional[float] = Query(None),
    max_ips: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(School)
    if min_ips is not None:
        query = query.filter(School.ips >= min_ips)
    if max_ips is not None:
        query = query.filter(School.ips <= max_ips)
    return query.all()

@router.get("/schools/{uai}", tags=["schools"], response_model=SchoolOut)
def get_school_by_uai(
    uai: str,
    db: Session = Depends(get_db)
):
    school = db.query(School).filter(School.uai == uai).first()
    if not school:
        raise HTTPException(status_code=404, detail="École non trouvée")
    return school

@router.delete("/schools/{uai}", tags=["schools"])
def delete_school_by_uai(
    uai: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
) -> Dict[str, str]:
    school = db.query(School).filter(School.uai == uai).first()
    if not school:
        raise HTTPException(status_code=404, detail="École non trouvée")
    
    db.delete(school)
    db.commit()
    return {"message": f"✅ École avec UAI {uai} supprimée avec succès par {user}."}
