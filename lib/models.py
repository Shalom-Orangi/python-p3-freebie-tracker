from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', back_populates='company')
    devs = relationship('Dev', secondary='dev_freebies')

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship('Freebie', back_populates='dev')
    companies = relationship('Company', secondary='dev_freebies')
    
    def received_one(self, item_name):
        
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        if freebie.dev == self:
            freebie.dev = other_dev
            return True
        return False
    
    def __repr__(self):
        return f'<Dev {self.name}>'
    
class Freebie(Base):
    __tablename__='freebies'

    id=Column(Integer(),primary_key=True)
    item_name=Column(String())
    value=Column(Integer())

    dev_id=Column(Integer(),ForeignKey('dev.id'))
    company_id=Column(Integer(),ForeignKey('company.id'))

    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def ___repr__(self):
        return f'<Dev{self.item_name}>'
    
class DevFreebie(Base):
    __tablename__ = 'dev_freebies'
    dev_id = Column(Integer, ForeignKey('devs.id'), primary_key=True)
    freebie_id = Column(Integer, ForeignKey('freebies.id'), primary_key=True)
