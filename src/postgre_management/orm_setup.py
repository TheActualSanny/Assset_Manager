from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Agency(Base):
    '''
        
    '''
    __tablename__ = 'agencies'
    agency_name = Column(String(50), primary_key = True)

class Project(Base):
    '''
        Contains the name column and
        a foreign key to a corresponding agency.
        This will be used to validate the passed parameters in the endpoints.
    '''
    __tablename__ = 'projects'
    project_name = Column(String(50), primary_key = True)
    corresponding_agency = Column(String(50), ForeignKey('agencies.agency_name'))
