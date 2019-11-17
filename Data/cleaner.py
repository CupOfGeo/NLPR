"""
clearn tool for pre procesing the lyrics
"""
import io
import re
from num2words import num2words
from os import path



folder_name = input("folder name?")


songs = []
ln = ' '
#gets all the songs to be processed
with open(folder_name + "/song_list.txt",'r', encoding="utf-8") as sl:
    while not(ln == ''):
        ln = sl.readline()
        songs.append(ln.rstrip())
sl.close()
songs.remove('')

#helper functions
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

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)



#op = open("RAW_bars.txt",'w+')
dic = {}
artdic = {}
text = ''
clean_text = ''
#s = input('eminem_song_name \n')
#s = 'eminem_' + s
#songs = [s]
#print(songs)
for fil in songs:	
	if(path.exists('cleanlyrics/' + fil + '.txt')):
		continue
	print('\n' + fil)

	#use = input('should we use this song n for no or enter? \n')
	#if(use == 'n'):
	#	continue
	
	with open(folder_name + '/lyrics/' + fil + '.txt', 'r', encoding="utf-8") as f:
		#reads file and turns utf-8 into ascii
		text = f.read() #+=
	#	text = text.decode('utf-8')
	#	text = text.encode("ascii","ignore")
		text = text.lower()
		#replaces all nums
		print("----------------before text -----------------------\n" + text)
		text = remove_non_ascii(text)
		for nums in re.findall(r'[0-9]+',text):
			#print(nums)
			text = re.sub(r'[0-9]+', num2words(nums), text, count=1)
		text = re.sub('(?s)<i>\[chorus(.*?)(?:(?:\r*\n){2})', "", text)
		text = re.sub('</div>', '', text)
		text = re.sub('<br/>', '', text)	

		'''	
		artists = re.findall('<i>\[(.*?)\]</i>',  text)
		print(artists)
		artdic = allowedArtists(artists, artdic)
		for key in artdic:
			group = re.search("'(?s)<i>\['+ key +'(.*?)(?:(?:\r*\n){2})'",text)
			print(group.span())
			if artdic[key] == 0:
				text = re.sub('(?s)<i>\['+ key +'(.*?)(?:(?:\r*\n){2})', "", text)

		'''
		dic = WordCount(text,dic)
		text = re.sub('<i>.*</i>', '', text)
		
		print("+++++++++++++++++++++After++++++++++++++++\n" + text)
		#for word in text.split():
			#print(word)
	op = open(folder_name + '/cleanlyrics/' + fil + '.txt', 'w+')
	op.write(text)
	op.close()
mega = open(folder_name + '/mega_bars.txt', 'a+')
merg = input("merge all files?")
if(merg == 'y'):
	for fil in songs:
		with open(folder_name + '/cleanlyrics/' + fil + '.txt', 'r', encoding="utf-8") as f:
			text = f.read()
			mega.write(text)
		

mega.close()













