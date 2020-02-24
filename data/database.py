from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Word, CountMessage, CountWord

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


def upgrade_message_count(array):
	session = Session()

	num_rows_deleted = session.query(CountMessage).delete()
	for i in range(0, len(array)):
		session.add(CountMessage(id=i, count=array[i]))

	session.commit()


def upgrade_word_count(array):
	session = Session()

	num_rows_deleted = session.query(CountWord).delete()
	for i in range(0, len(array)):
		session.add(CountWord(id=i, count=array[i]))

	session.commit()


def upgrade_database():
	import data.processing

	dataset = data.processing.process_word_count()
	upgrade_words(dataset)

	message_count = data.processing.message_count()
	upgrade_message_count(message_count)

	word_count = data.processing.word_count()
	upgrade_word_count(word_count)
