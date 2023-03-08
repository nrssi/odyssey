from .db_models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .logger import logger

DB_URL = "sqlite:///./uuid_details.db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def register_user(name: str, address: str, contact_ph: int, email: str, fingerprint_features: bytes, face_features: bytes) -> bool:
    db = SessionLocal()
    user = Citizens(name=name, address=address, contact_ph=contact_ph, email=email,
                    fingerprint_features=fingerprint_features, face_features=face_features)
    try:
        db.add(user)
        db.commit()
    except Exception as e:
        logger.error(f"Can't register user due to => {e}")
        return False
    return True


def register_candidate(uuid: int, party_id: int) -> bool:
    db = SessionLocal()
    citizen = db.query(Citizens).filter(Citizens.uuid == uuid).first()
    if not citizen:
        logger.error(f"No citizen with {uuid} exists")
        return False
    else:
        candidate = Candidate(
            uuid=citizen.uuid, name=citizen.name, party_id=party_id)
        try:
            db.add(candidate)
            db.commit()
        except Exception as e:
            logger.error(f"Can't register candidate due to => {e}")
            return False
    return True


def register_party(name: str) -> bool:
    db = SessionLocal()
    party = Politicalparties(name=name)
    try:
        db.add(party)
        db.commit()
    except Exception as e:
        logger.error(f"Can't register party due to => {e}")
        return False
    return True


def fetch_user(id: int) -> Citizens | None:
    db = SessionLocal()
    try:
        user = db.query(Citizens).filter(Citizens.id == id).first()
        return user
    except Exception as e:
        logger.error(
            f"Citizen with ID {id} doesn't exist, Additional info : {e}")
        return None


def fetch_candidate(id: int) -> Candidate | None:
    db = SessionLocal()
    try:
        user = db.query(Candidate).filter(Candidate.id == id).first()
        return user
    except Exception as e:
        logger.error(
            f"Citizen with ID {id} doesn't exist, Additional info : {e}")
        return None
