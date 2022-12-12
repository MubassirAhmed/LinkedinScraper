from base import Base, engine
# Import the PprRawAll table
from tables import PprRawAll

# Create the table in the database
if __name__ == "__main__":
    Base.metadata.create_all(engine)
