# create_tables.py

from sqlalchemy import inspect
from app.model_db import ResultModel
from app.database import engine, Base

# Check if the tables already exist
inspector = inspect(engine)
tables_to_create = []

# Add tables to the list if they do not exist
if not inspector.has_table(ResultModel.__tablename__):
    tables_to_create.append(ResultModel.__table__)

# Create tables if there are any to create
if tables_to_create:
    Base.metadata.create_all(bind=engine, tables=tables_to_create)
    print("Tables created successfully.")
else:
    print("Tables already exist. Skipping creation.")