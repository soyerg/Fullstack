from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from bdd.database import SessionLocal
from bdd.models import School
from dependencies import get_current_user
from typing import Optional

router = APIRouter()

# Dépendance : session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 1. Toutes les écoles (avec filtres facultatifs)
@router.get("/schools", tags=["schools"])
def get_all_schools(
    db: Session = Depends(get_db),

):
    query = db.query(School)

    return query.all()

# 🔹 2. Écoles par plage d’IPS
@router.get("/schools/ips", tags=["schools"])
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

# 🔹 3. Une école par UAI
@router.get("/schools/{uai}", tags=["schools"])
def get_school_by_uai(
    uai: str,
    db: Session = Depends(get_db)
):
    school = db.query(School).filter(School.uai == uai).first()
    if not school:
        raise HTTPException(status_code=404, detail="École non trouvée")
    return school

# 🔐 4. Supprimer une école par UAI (protégé par JWT)
@router.delete("/schools/{uai}", tags=["schools"])
def delete_school_by_uai(
    uai: str,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    school = db.query(School).filter(School.uai == uai).first()
    if not school:
        raise HTTPException(status_code=404, detail="École non trouvée")
    
    db.delete(school)
    db.commit()
    return {"message": f"✅ École avec UAI {uai} supprimée avec succès par {user}."}
