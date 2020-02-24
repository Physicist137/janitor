from sqlalchemy import create_engine
engine = create_engine('sqlite:///janitor.db', echo=True)

def init_db():
	from . import models
	models.Base.metadata.create_all(bind=engine)
