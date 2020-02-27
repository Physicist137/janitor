from data.models import Message, Word, CountMessage, CountWord
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


def word_count():
	session = Session()
	class_array_size = 1 + max_class()
	word_count = [0] * class_array_size

	for count in session.query(Word.count):
		arr = ast.literal_eval(count[0])

		for i in range(0, len(word_count)):
			word_count[i] += arr[i]
		

	return word_count


def load_message_count():
	session = Session()

	class_array_size = 1 + max_class()
	message_count = [0] * class_array_size
	for count in session.query(CountMessage).all():
		message_count[count.id] = count.count

	return message_count


def load_word_count():
	session = Session()

	class_array_size = 1 + max_class()
	word_count = [0] * class_array_size
	for count in session.query(CountWord).all():
		word_count[count.id] = count.count

	return word_count


def load_all_word_dataset():
	session = Session()

	dataset = dict()
	for word,count in session.query(Word.word, Word.count):
		dataset[word] = ast.literal_eval(count)

	return dataset


def load_one_word_dataset(word):
	session = Session()
	result = session.query(Word).filter(Word.word == word).first()
	if result is None: return None
	else: return ast.literal_eval(result.count)
	

def load_some_word_dataset(words):
	session = Session()

	dataset = dict()
	for word in words:
		result = session.query(Word).filter(Word.word == word).first()
		if result is not None:
			dataset[result.word] = ast.literal_eval(result.count)
	
	return dataset	


def load_word_dataset(arg = None):
	if arg is None: return load_all_word_dataset()
	elif isinstance(arg, list): return load_some_word_dataset(arg)
	elif isinstance(arg, str): return load_one_word_dataset(arg)
	else: return None
