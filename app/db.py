from sqlalchemy import create_engine
from app.config import DATABASE_URL

engine = create_engine("postgresql://postgres:postgres@localhost:5433/careerdb")
