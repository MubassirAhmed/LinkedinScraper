from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
# Import the function required
from sqlalchemy.orm import column_property
import re


Base = declarative_base()

class PprRawAll(Base):
    __tablename__ = "postings_raw"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(55))
    appsPerHr = Column(String(255))
    noApplicants = Column(String(55))
    postedTimeAgo = Column(String(55))
    company = Column(String(55))
    job_link = Column(String(55))
    description = Column(String(55))
    criterion = Column(String(55))
    industry = Column(String(55))
    typeOfJob = Column(String(55))
    
    # Create a unique transaction id
    transaction_id = column_property(
        re.search("\d.*\?",job_link)
    )


    

class PprRawAll(Base):
    __tablename__ = "ppr_clean_all"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(55))
    appsPerHr = Column(Integer)
    noApplicants = Column(Integer)
    company = Column(String(55))
    job_link = Column(String(55))
    description = Column(String(55))
    criterion = Column(String(55))
    industry = Column(String(55))
    typeOfJob = Column(String(55))
    
    # Create a unique transaction id
    # all non-string columns are casted as string
    transaction_id = column_property(
        re.search("\d.*\?",job_link)
    )
