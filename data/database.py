from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///janitor.db', echo=True)
Session = sessionmaker(bind=engine)

def init_db():
	from . import models
	models.Base.metadata.create_all(bind=engine)
