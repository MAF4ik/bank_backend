from sqlalchemy import create_engine

db_url = 'postgresql://postgres:21M05A06F@localhost:5432/bank_db'
engine = create_engine(db_url, echo=False)
