"""
Dylan Zucker, Ryan Pasculano, Melanie Cheng & David Schwartz
CSCI 379 - Fall 2018
Intro to AI & Cog Sci
Final Project

This file trains a model to generate Harry Potter 7 type text.
"""
"""
SWIPE LIFE
Geirge Mazzeo's Slimshady clone
"""


# TODO Make more directories to clean the directory up

import re
import string
from keras.callbacks import ModelCheckpoint
from random import randint
from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from numpy import array
from pickle import dump
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
import numpy
import matplotlib.pyplot as plt


#this checks that im using the gpu 
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())



def make_model(num_words, seq_length):
	'''

	:param num_words:
	:param seq_length:
	:return:
	'''
	# TODO: Compare with deeper model / wider model / less deep model / less wide model with graph of val_losses
	#TODO make bigger?
	model = Sequential()
	model.add(Embedding(num_words, 50, input_length=seq_length)) # Input layer num_words is the vocab size, 50 = outputs_dim, input_len= X.shape?? but neede for Dense layers )
	model.add(LSTM(150, return_sequences=True)) #Long short term memory 150 outputnodes activation is tanh
	#return_sequences: Boolean. Whether to return the last output in the output sequence, or the full sequence. from keras
	#also to look into convolutionalLSTM keras.layers.ConvLSTM2D(
	model.add(LSTM(150))
	model.add(Dense(150, activation='relu'))
	model.add(Dense(num_words, activation='softmax'))
	return model

def generation(model):
	'''

	:param model:
	:param tokenizer:
	:return:
	'''
	in_filename = 'raw_bars.txt'
	text = get_text_from_file(in_filename)
	'''
	text = ''
	for fil in songs:
		if not('skit' in fil):
			text += get_text_from_file('lyrics/' + fil + '.txt')
	'''
	

	
	choice = input("Would you like to use random text? (Y) for yes or anything else to input your own: ")
	if choice == "y" or choice == "Y":
		lines = text.split('\n')
		seq_length = len(lines[0].split()) - 1
		seed_text = lines[randint(0, len(lines))]
	else:
		seed_text = input("Input your seed text needs to be length 50 words: ")
		seq_length = len(seed_text.split()[:50])

#	model.load_weights("../weights/text_generator_word_based_" + FILE_PREFIX + ".h5")
#	tokenizer = load(open('tokenizer_' + FILE_PREFIX + '.pkl', 'rb'))
	model.load_weights("weights-word_based.best.hdf5")
	tokenizer = load(open('tokenizer' + '.pkl', 'rb'))


	# generate new text
	num_generated = int(input("How many words would you like to generate? "))
	generated = generate_seq(model, tokenizer, seq_length, seed_text, num_generated)
	generated = generated.replace('zzz', '\n')
	return seed_text, generated


# turn a doc into clean tokens
def clean_doc(doc):
	'''

	:param doc:
	:return:
	'''
	# replace '--' with a space ' '
	doc = doc.replace('--', ' ')
	# split into tokens by white space
	tokens = re.findall(r'\S+|\n',doc)
	tokens = [x if (not x == '\n') else 'zzz' for x in tokens]
	# remove punctuation from each token
	table = str.maketrans('', '', string.punctuation)
	tokens = [w.translate(table) for w in tokens]
	# remove remaining tokens that are not alphabetic
	tokens = [word.lower() for word in tokens if word.isalpha()]
	return tokens



def graph_results(history):
	"""

	:param history:
	:return:
	"""
	# Plot accuracy
	f = plt.figure()
	plt.plot(history.history["accuracy"])
	plt.title("Accuracy of the Model")
	plt.xlabel("Epoch")
	plt.ylabel("Accuracy")
	plt.show()
#	f.savefig("../figures/acc.pdf", bbox_inches="tight")
	f.savefig("acc.pdf", bbox_inches = "tight")



	# Plot Loss
	f = plt.figure()
	plt.plot(history.history['loss'])
	plt.title('Loss of the Model')
	plt.xlabel('Epoch')
	plt.ylabel('Loss')
	plt.show()
	f.savefig("loss.pdf", bbox_inches="tight")

	f = plt.figure()
	plt.plot(history.history['accuracy'])
	plt.plot(history.history['loss'])
	plt.title('Loss vs Acc')
	plt.ylabel('Loss/ACC')
	plt.xlabel('Epoch')
	plt.legend(['Acc', 'Loss'], loc='upper left')
	plt.show()
	f.savefig("loss_acc.pdf", bbox_inches="tight")


# save tokens to file, one dialog per line
def save_doc(lines, filename):
	'''
	:param lines:
	:param filename:
	:return:
	'''
	data = '\n'.join(lines)
	with open(filename, "w") as file:
		file.write(data)


# TODO Write more documentation and cite shouts to the boys
def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
	'''
	Generate a sequence from a language model
	:param model:
	:param tokenizer:
	:param seq_length:
	:param seed_text:
	:param n_words:
	:return:
	'''
	# result = list()
	result = []
	in_text = seed_text
	# generate a fixed number of words
	for _ in range(n_words):
		encoded = tokenizer.texts_to_sequences([in_text])[0]
		encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
		yhat = model.predict_classes(encoded, verbose=0)

		out_word = ''
		for word, index in tokenizer.word_index.items():
			if index == yhat:
				out_word = word
				break

		in_text += ' ' + out_word
		result.append(out_word)
	return ' '.join(result)


def get_text_from_file(filename):
	with open(filename, "r") as file:
		text = file.read()
	return text


def make_sequences():
	'''
	:return:
	'''
	in_filename = 'raw_bars.txt'
	text = get_text_from_file(in_filename)
	'''
	text = ''
	for fil in songs:
		if not ('skit' in fil):
                	text += get_text_from_file('lyrics/' + fil + '.txt')
	'''

	tokens = clean_doc(text)

	# organize into sequences of tokens
	length = 50 + 1
	sequences = list()
	for i in range(length, len(tokens)):
		# select sequence of tokens
		seq = tokens[i - length:i]
		# convert into a line
		line = ' '.join(seq)
		# store
		sequences.append(line)

	# save sequences to file
#	out_filename = FILE_PREFIX + '_sequences.txt'
	out_filename = 'Slimshady_' + '_sequences.txt'
	save_doc(sequences, out_filename)
	return sequences


def main():
	'''

	:return:
	'''
	lines = make_sequences()
	#
	# in_filename = FILE_PREFIX + '_sequences.txt'
	# text = get_text_from_file(in_filename)
	# lines = text.split('\n')
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	sequences = tokenizer.texts_to_sequences(lines)
	vocab_size = len(tokenizer.word_index) + 1
	# separate into input and output
	sequences = array(sequences)
	X, y = sequences[:, :-1], sequences[:, -1]
	y = to_categorical(y, num_classes=vocab_size)
	seq_length = X.shape[1]
	print(X.shape[1])
	print(vocab_size)
	model = make_model(vocab_size, seq_length)
	filepath = "weights-word_based.best.hdf5" # Maybe put this on top
#	checkpoint = ModelCheckpoint(filepath, verbose=1,mode='max')  # Save weights after each epoch maybe make it only if it gets better.
	checkpoint = ModelCheckpoint(filepath, monitor='loss',
                             verbose=1, save_best_only=True,
                             mode='min')
	
	from keras.callbacks import ReduceLROnPlateau 
	reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=1, min_lr=0.001)
	




	dump(tokenizer, open('tokenizer' + '.pkl', 'wb'))
	callbacks_list = [checkpoint,reduce_lr]
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	choice = input("Input (Y) if you want to train. Input anything else if you just want to generate text: ")
	if choice == "y" or choice == "Y":

		history = model.fit(X, y, batch_size=128, epochs=100, callbacks=callbacks_list)  # TODO VAL SPLIT?

		# TODO: Maybe put weights file name on top as constant
		model.save_weights('text_generator_word_based_' + 'SS_LP' + '.h5')  # Save the weights after training

		graph_results(history)





	else:
		again = input("another one? y,n").lower()
		while again == 'y' :
			seed_text, generated = generation(model)
			print(" ".join(seed_text.split()[:50]))
			print()
			print(generated)


main()

