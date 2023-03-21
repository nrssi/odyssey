from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


class Citizens(Base):
    __tablename__ = 'citizens'

    name = Column(Text, nullable=False)
    uuid = Column(Integer, primary_key=True)
    address = Column(Text)
    contact_ph = Column(Integer)
    email = Column(Text)
    fingerprint = Column(LargeBinary)
    face = Column(LargeBinary)
    father_name = Column(Text)
    mother_name = Column(Text)
    dob = Column(Text)

    candidate = relationship('Candidate', back_populates='citizens')


class PoliticalParties(Base):
    __tablename__ = 'political_parties'

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
    uuid = Column(ForeignKey('citizens.uuid'))
    party_id = Column(ForeignKey('political_parties.party_id'))
    name = Column(Text)

    party = relationship('PoliticalParties', back_populates='candidate')
    citizens = relationship('Citizens', back_populates='candidate')
