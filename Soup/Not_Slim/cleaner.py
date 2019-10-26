"""
clearn tool

import inflect
p = inflect.engine()
p.number_to_word(99)
-> ninety-nine
"""
import io
import re
from num2words import num2words
from os import path

songs = []
ln = ' '
with open("song_list.txt",'r', encoding="utf-8") as sl:
    while not(ln == ''):
        ln = sl.readline()
        songs.append(ln.rstrip())
sl.close()
songs.remove('')

def get_text_from_file(filename):
        with open(filename, "+") as file:
                text = file.read()
        return text


def WordCount(str, lcDict):
	list1=str.split()
	for l in list1:	
		if l in lcDict:
			lcDict[l] +=1
		else:
			lcDict[l]= 1
	return lcDict
	
def LetterCount(str, lcDict):
	list1=list(str)
	for l in list1:	
		if l in lcDict:
			lcDict[l] +=1
		else:
			lcDict[l]= 1
	return lcDict
	
def allowedArtists(list1, lcDict):
	for l in list1:
		if ('chorus' in l):
			lcDict[l] = 0
		if l not in lcDict:
			print(l)
			allow = input('		allow to accepted artists y/n,sound?')
			if (allow == 'y'):
				lcDict[l] = 1
			elif(allow == 'n'):
				lcDict[l] = 0
			else:
				lcDict[l] = 2 # ad lib sound
	print(lcDict)
	return lcDict


#op = open("RAW_bars.txt",'w+')
dic = {}
artdic = {}
text = ''
clean_text = ''
#s = input('eminem_song_name \n')
#s = 'eminem_' + s
#songs = [s]
#print(songs)
for fil in songs	
	if(path.exists('cleanlyrics/' + fill + '.txt')):
		continue
	print(fil)

	use = input('should we use this song n for no or enter? \n')
	if(use == 'n'):
		continue
	
	with open('lyrics/' + fil + '.txt', 'r', encoding="utf-8") as f:
		
		text = f.read() #+=
		text = text.lower()
		for nums in re.findall(r'[0-9]+',text):
			print(nums)
			text = re.sub(r'[0-9]+', num2words(nums), text, count=1)
					
		text = re.sub('(?s)<i>\[chorus(.*?)(?:(?:\r*\n){2})', "", text)
		text = re.sub('</div>', '', text)
		text = re.sub('<br/>', '', text)	

	
		artists = re.findall('<i>\[(.*?)\]</i>',  text)
		print(artists)
		artdic = allowedArtists(artists, artdic)
		for key in artdic:
			if artdic[key] == 0:
				text = re.sub('(?s)<i>\['+ key +'(.*?)(?:(?:\r*\n){2})', "", text)
		dic = WordCount(text,dic)
		text = re.sub('<i>.*</i>', '', text)
		
		#for word in text.split():
			#print(word)
	
#print(text)
#print(sorted(dic.items(), key = lambda x: x[1]))
	op.write(text)
op.close()
f.close()



class TxtEditor:
	def __init__(self, filename, edit='+'):
		self.filename = filename
		fp = open(filename, edit)
		self.doc = fp.read()
		fp.close()

	def Print(self):
		i = 0
		text = self.doc.split('\n')
		for line in text:
			print(str(i) + ' : ' + line)

	def Edit(self):
		print('ok') 
