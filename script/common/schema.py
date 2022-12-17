from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
#from sqlalchemy.orm import column_property


Base = declarative_base()

class PprRawAll(Base):
    __tablename__ = "postings_raw"
    
    job_id = Column(Integer, primary_key=True)
    title = Column(String(55))
    appsPerHr = Column(Integer)
    noApplicants = Column(Integer)
    postedTimeAgo = Column(String(55))
    company = Column(String(55))
    job_link = Column(String(55))
    description = Column(String(55))
    typeOfJob = Column(String(55))
    """
    # Create a unique transaction id
    job_id = column_property(
        re.search("\d.*\?",job_link)
    )"""
    

class PprCleanAll(Base):
    __tablename__ = "postings_clean"
    
    job_id = Column(Integer, primary_key=True)
    title = Column(String(55))
    appsPerHr = Column(Integer)
    noApplicants = Column(Integer)
    company = Column(String(55))
    job_link = Column(String(55))
    description = Column(String(55))
    typeOfJob = Column(String(55))
    """
    # Create a unique transaction id
    # all non-string columns are casted as string
    job_id = column_property(
        re.search("\d.*\?",job_link)
    )"""
