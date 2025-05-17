# app/schemas.py
from pydantic import BaseModel
from typing import Optional


class SchoolOut(BaseModel):
    id: int
    rentree_scolaire: Optional[str]
    academie: Optional[str]
    code_du_departement: Optional[str]
    departement: Optional[str]
    uai: Optional[str]
    nom_de_l_etablissment: Optional[str]
    code_insee_de_la_commune: Optional[str]
    nom_de_la_commune: Optional[str]
    secteur: Optional[str]
    ips: Optional[float]

    class Config:
        from_attributes = True
