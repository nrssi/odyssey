from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Table, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


class Citizens(Base):
    __tablename__ = 'citizens'

    name = Column(Text, nullable=False)
    address = Column(Text)
    contact_ph = Column(Integer)
    email = Column(Text)
    fingerprint = Column(LargeBinary)
    face = Column(LargeBinary)
    father_name = Column(Text)
    mother_name = Column(Text)
    dob = Column(Text)
    aadhar_number = Column(Integer, primary_key=True)

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

    id = Column(Integer, primary_key=True)
    aadhar_number = Column(ForeignKey('citizens.aadhar_number'))
    party_id = Column(ForeignKey('political_parties.party_id'))

    citizens = relationship('Citizens', back_populates='candidate')
    party = relationship('PoliticalParties', back_populates='candidate')
