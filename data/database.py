from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Word, ClassCount

engine = create_engine('sqlite:///janitor.db', echo=True)
Session = sessionmaker(bind=engine)

def create_database():
	from . import models
	models.Base.metadata.create_all(bind=engine)


def upgrade_words(dataset):
	session = Session()

	num_rows_deleted = session.query(Word).delete()
	for word in dataset:
		session.add(Word(word=word, count=str(dataset[word])))

	session.commit()


def upgrade_count(array):
	session = Session()

	num_rows_deleted = session.query(ClassCount).delete()
	for i in range(0, len(array)):
		session.add(ClassCount(id=i, count=array[i]))

	session.commit()


def upgrade_database():
	from data.processing import process_word_count
	dataset = process_word_count()
	upgrade_words(dataset)

	from data.processing import message_count
	array_count = message_count()
	upgrade_count(array_count)
