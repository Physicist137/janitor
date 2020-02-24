from data.models import Message, Word
from data.database import Session
from sqlalchemy.sql.expression import func


def word_count():
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


	return (dataset)
