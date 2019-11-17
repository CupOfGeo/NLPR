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
from keras.preprocessing.text import Tokenizer

import os

INPUT_SIZE=40
OUTPUT_LEN=100
EPOCHS=150

'''
gets the cleaned lyrics from the one large text file Em-bars.txt
makes the sequences and outputs them as outputBars.txt
'''
def get_bars():
	outFileName = 'outputBars.txt'
	for inFile in os.listdir("cleanlyrics"):
		#print(inFile) 
		#inFile = 'mega_bars.txt' # cleaned input file
		#for inFile in /cleanlyrics songs.txt
		file = open('cleanlyrics/' + inFile, 'r') # open file
		text = file.read() # read file into text array
		file.close() # close file
		textArr = clean_doc(text)

		# make sequences of 30 words with 1 output word
		length = INPUT_SIZE + 1
		bars = list()
		# splitting words into sequences called bars
		for i in range(length, len(textArr)):
			bar = textArr[i-length:i]
			line = ' '.join(bar)
			bars.append(line)
		#save these bars to an output file
		#save to sequence folder?
		
		append_doc(bars, outFileName)
	return bars


'''
save file function
'''
def append_doc(lines, fileName):
  # save sequences of text to a file
  data = '\n'.join(lines)
  file = open(fileName,"a+") 
  file.write(data)
  file.close()



'''
save file function
'''
def save_doc(lines, fileName):
	# save sequences of text to a file
	data = '\n'.join(lines)
	file = open(fileName,"w+") 
	file.write(data)
	file.close()


'''
The Neurla net model 
2 LSTM layers of 100 nodes each
Dense layer of 100 nodes with relu activation
Dense layer softmax activation
'''
def make_model(vocab_size, seq_length):
	model = Sequential()
	model.add(Embedding(vocab_size, 30, input_length =seq_length))
	# embedding takes size of vocab and input sequence length
	# takes size of embedding vector space (how many dimensions will be used to represent each word)
	model.add(LSTM(100, return_sequences=True)) #LSTM with 100 memory cells
	model.add(LSTM(100))
	model.add(Dense(100, activation='relu'))
	model.add(Dense(vocab_size, activation= 'softmax'))
	model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy']) # compile network
	# TODO model is compiled specifying the categorical cross entropy loss needed to fit the model
	# Should be using our own custom word similarity loss function 
	model.summary() 
	return model



'''
turns lines to tokens
returns the tokens
'''
def clean_doc(doc):
	# replace '--' with a space ' '
	doc = doc.replace('--', ' ')
	# split into tokens by white space
	tokens = re.findall(r'\S+|\n',doc)
	tokens = [word.replace('\n', 'zzzzz') for word in tokens]
	tokens = [word.lower() for word in tokens if word.isalpha()]
	return tokens


'''
If the model is not being trained
This is where the model outputs the  100 words based on a seedText of 30 words
'''
def use_model(seedTextFile):
	seq_length = INPUT_SIZE
	model = load_model('model.h5') #loads the keras model
	tokenizer = load(open('tokenizer.pkl', 'rb'))
	model.load_weights("bestweights.hdf5") # loads weights

	# need seed text as input to the model, get user input from file
	file = open(seedTextFile, 'r')
	seed_text = file.read()
	file.close()
	print("Seed text is: ", seed_text, "\n")
	output = generate_sequence(model, tokenizer, seq_length, seed_text, OUTPUT_LEN)
	print("New text is: ", output, "\n")
 



'''
Generates the 100 words 
predicts a word called target from 30 words 
target is a number that must be looked up in a dictionary to find the actual word
adds the target_word to the output to be returned to use_model
'''
def generate_sequence(model, tokenizer, seq_length, seed_text, n):
	# generate a sequence of new words of length n based on the training data
	result = list()
	input_text = seed_text
	print(input_text)

	#loop to generate n words
	for i in range(n):
		# need to encode seed text the same as model was encodeed
		encoded = tokenizer.texts_to_sequences([input_text])[0]
		encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre') # after adding new word, need to truncate to given length
		# predict probabilities for each word in dictionary, pick the one with highest probabilities
		target = model.predict_classes(encoded, verbose = 0)
		# need to find target within tokens to print the best word
		target_word = ''
		for word, index in tokenizer.word_index.items():
			if index == target:
				target_word = word
				break
		input_text += ' ' + target_word
		result.append(target_word)
	return ' '.join(result)




def graph_results(history):
	"""

	:param history:
	:return:
	"""
	# Plot accuracy and loss
	f = plt.figure()
	plt.plot(history.history['accuracy'])
	plt.plot(history.history['loss'])
	plt.title('Loss vs Acc')
	plt.ylabel('Loss/ACC')
	plt.xlabel('Epoch')
	plt.legend(['Acc', 'Loss'], loc='upper left')
	f.savefig("loss_acc.pdf", bbox_inches="tight")





'''
main method to train model
'''
def main():
	use_model('seedText.txt')
main()

