from data.processing import process_message, load_word_count, load_message_count, load_word_dataset

def naive_probability(message, smoothness=1):
	processed = process_message(message)
	word_dataset = load_word_dataset(processed)
	message_count = load_message_count()
	word_count = load_word_count()
	arr_size = len(word_count)

	result = [1] * arr_size
	for word in word_dataset:
		probability = sum(word_dataset[word]) / sum(word_count)
		for i in range(0, arr_size):
			conditional = word_dataset[word][i] / word_count[i]
			result[i] *= conditional / probability

	for i in range(0, arr_size):
		class_probability = message_count[i] / sum(message_count)
		result[i] *= class_probability
	
	return result
