from sqlalchemy import Column, Integer, String, Float
from .database import Base

class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True, index=True)
    rentree_scolaire = Column(String)
    academie = Column(String)
    code_du_departement = Column(String)
    departement = Column(String)
    uai = Column(String, unique=True)
    nom_de_l_etablissment = Column(String)
    code_insee_de_la_commune = Column(String)
    nom_de_la_commune = Column(String)
    secteur = Column(String)
    ips = Column(Float)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
