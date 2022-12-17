# Import the modules required
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

# Create the engine
engine = create_engine(
    'snowflake://{user}:{password}@{account_identifier}/'.format(
        user='mvbashxr',
        password='ReLife!23',
        account_identifier='ep66367.ca-central-1.aws',
    )
)
# Initialize the session
session = Session(engine)

# Initialize the declarative base
Base = declarative_base()
