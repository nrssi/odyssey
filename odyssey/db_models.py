from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


class Citizens(Base):
    __tablename__ = 'citizens'

    name = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    fingerprint_features = Column(LargeBinary, nullable=False)
    face_features = Column(LargeBinary, nullable=False)
    uuid = Column(Integer, primary_key=True)
    contact_ph = Column(Integer)
    email = Column(Text)

    candidate = relationship('Candidate', back_populates='citizens')


class Politicalparties(Base):
    __tablename__ = 'politicalparties'

    party_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

    candidate = relationship('Candidate', back_populates='party')


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Candidate(Base):
    __tablename__ = 'candidate'

    candidate_id = Column(Integer, primary_key=True)
    uuid = Column(ForeignKey('citizens.uuid', ondelete='CASCADE'), nullable=False)
    party_id = Column(ForeignKey('politicalparties.party_id', ondelete='CASCADE'))
    name = Column(Text)

    party = relationship('Politicalparties', back_populates='candidate')
    citizens = relationship('Citizens', back_populates='candidate')
