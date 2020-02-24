from data.models import Message, Word
from data.database import Session
from sqlalchemy.sql.expression import func
import ast

def process_message(message):
	words = message.replace('  ', ' ') \
		.replace('?', '') \
		.replace('!', '') \
		.replace(',', '') \
		.replace('.', '') \
		.replace('`', '') \
		.replace('\'', '') \
		.replace('\"', '') \
		.lower() \
		.split(' ')

	return words


def max_class():
	session = Session()
	class_max = session.query(func.max(Message.classification)).first()[0]
	return class_max


def process_word_count():
	session = Session()

	class_array_size = 1 + max_class()
	class_array = [0] * class_array_size

	dataset = dict()
	for content, classification in session.query(Message.content, Message.classification):
		words = process_message(content)

		for word in words:
			if word not in dataset:
				array = class_array[:]
				array[classification] = 1
				dataset[word] = array
			
			else:
				dataset[word][classification] += 1


	return dataset


def message_count():
	session = Session()
	class_array_size = 1 + max_class()
	message_count = [0] * class_array_size

	for classification in session.query(Message.classification):
		c = classification[0]
		message_count[c] += 1
		
	return message_count


def upgrade_words(dataset):
	session = Session()

	num_rows_deleted = session.query(Word).delete()
	for word in dataset:
		session.add(Word(word=word, count=str(dataset[word])))

	session.commit()


def load_all_word_count():
	session = Session()

	dataset = dict()
	for word,count in session.query(Word.word, Word.count):
		dataset[word] = ast.literal_eval(count)

	return dataset


def load_one_word_count(word):
	session = Session()
	result = session.query(Word).filter(Word.word == word).first()
	if result is None: return None
	else: return ast.literal_eval(result.count)
	

def load_some_word_count(words):
	session = Session()

	dataset = dict()
	for word in words:
		result = session.query(Word).filter(Word.word == word).first()
		if result is not None:
			dataset[result.word] = ast.literal_eval(result.count)
	
	return dataset	


def load_word_count(arg = None):
	if arg is None: return load_all_word_count()
	elif isinstance(arg, list): return load_some_word_count(arg)
	elif isinstance(arg, str): return load_one_word_count(arg)
	else: return None
