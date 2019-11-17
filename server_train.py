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

INPUT_SIZE=20
OUTPUT_LEN=100
EPOCHS=150

i = 1
for folders in os.listdir("Models"):
	print(str(i)+ ': '  + folders)
	i = i +1

folder_sel = 1
folder_sel = int(folder_sel) -1
model_dir = 'Models/' + os.listdir("Models")[folder_sel] + '/'
#Models/Slim/


'''
gets the cleaned lyrics from the one large text file Em-bars.txt
makes the sequences and outputs them as outputBars.txt
'''
def get_bars():
	
	test = True
	outFileName = model_dir +'Data/sequenceOutput.txt'
	if 'sequenceOutput.txt' in os.listdir(model_dir + 'Data'):
		os.remove(outFileName)
		print('removed old sequences')
	for inFile in os.listdir(model_dir + "Data/cleanlyrics"):
		#print(inFile)
		#inFile = 'mega_bars.txt' # cleaned input file
		#for inFile in /cleanlyrics songs.txt
		file = open(model_dir + 'Data/cleanlyrics/'  + inFile, 'r') # open file
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
		bars[len(bars)-1] = bars[len(bars)-1] + '\n'
		append_doc(bars, outFileName)

	f = open(outFileName,'r')
	bars = f.read()
	f.close()
	bars = bars.split('\n')
	del bars[-1]
	print(bars)
	return bars


'''
append file helper function
'''
def append_doc(lines, fileName):
	# save sequences of text to a file
	data = '\n'.join(lines)
	file = open(fileName,"a+")
	file.write(data)
	file.close()



'''
save file helper function
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
	#tokens = [word.replace('\n', 'zzzzz') for word in tokens]
	tokens = [word.lower() for word in tokens if word.isalpha()]
	return tokens




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
	f.savefig(model_dir + "loss_acc.pdf", bbox_inches="tight")





'''
main method to train model
retreaves sequences

'''
def main():
	bars = get_bars() # bars also written to outputBars.txt
	print(bars)
	# encode data so every word maps to a number
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(bars) # builds vocab / vocab_size
	print('fit to tokens')
	sequences = tokenizer.texts_to_sequences(bars) # converts from list of words to list of integers
	print(sequences)
	vocab_size = len(tokenizer.word_index)+ 1 # size of vocabulary
	print(vocab_size)
	#separate sequences into input and output elements
	sequences = array(sequences)
	x, y = sequences[:,:-1], sequences[:, -1] # dimensions of sequences array is incorrect, need to fix this

	# keras function to one hot encode output words for input output sequence pair
	y = to_categorical(y, num_classes = vocab_size)
	seq_length = x.shape[1] # embedding layer that specifies length of input sequences
	model = make_model(vocab_size, seq_length)
	weightfile = "bestweights.hdf5"

	checkpoint = ModelCheckpoint("bestweights.hdf5", monitor='loss', verbose=1, save_best_only=True, mode='min')
	#only saves output if the weights get better
	from keras.callbacks import ReduceLROnPlateau
	reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=1, min_lr=0.001)
	# stops from plateuing
	cbl = [checkpoint, reduce_lr]


	history = model.fit(x, y, batch_size = 128, epochs =EPOCHS, callbacks =cbl)
	model.save(model_dir + 'model.h5') # saving model to a file
	model.save_weights(model_dir + 'bestweights.hdf5')
	dump(tokenizer, open(model_dir + 'tokenizer.pkl', 'wb')) # save the tokenizer
	graph_results(history)
main()
