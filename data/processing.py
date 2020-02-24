from data.models import Message, Word
from data.database import Session
from sqlalchemy.sql.expression import func
import ast

def process_word_count():
	session = Session()

	class_max = session.query(func.max(Message.classification)).first()[0]
	class_array_size = class_max + 1
	class_array = [0] * class_array_size

	dataset = dict()
	for content, classification in session.query(Message.content, Message.classification):
		words = content.replace('  ', ' ') \
			.replace('?', '') \
			.replace('!', '') \
			.replace(',', '') \
			.replace('.', '') \
			.replace('`', '') \
			.replace('\'', '') \
			.replace('\"', '') \
			.lower() \
			.split(' ')
	
		for word in words:
			if word not in dataset:
				array = class_array[:]
				array[classification] = 1
				dataset[word] = array
			
			else:
				dataset[word][classification] += 1


	return dataset


def upgrade_database(dataset):
	session = Session()

	num_rows_deleted = session.query(Word).delete()
	for word in dataset:
		session.add(Word(word=word, count=str(dataset[word])))

	session.commit()


def load_word_count():
	session = Session()

	dataset = dict()
	for word,count in session.query(Word.word, Word.count):
		dataset[word] = ast.literal_eval(count)

	return dataset
