"""
clearn tool

import inflect
p = inflect.engine()
p.number_to_word(99)
-> ninety-nine
"""


songs = []
ln = ' '
with open("song_list.txt",'r') as sl:
    while not(ln == ''):
        ln = sl.readline()
        songs.append(ln.rstrip())
sl.close()
songs.remove('')

def get_text_from_file(filename):
        with open(filename, "+") as file:
                text = file.read()
        return text



def LetterCount(str):
	list1=list(str)
	lcDict= {}
	for l in list1:	
		if l in lcDict:
			lcDict[l] +=1
		else:
			lcDict[l]= 1
	print(sorted(lcDict.items(), key = lambda x: x[1]))



text = ''
clean_text = ''
for fil in songs:
	if not('skit' in fil):
		with open('lyrics/' + fil + '.txt') as f:
			text += f.read()
#print(text.rstrip())
text = text.lower()
text = text.split('\n')
while(1==1):
	try:
		text.remove('')
	except:
		break
#print(text)
#text is a list of bars
new_text = ''
list1 = []
for line in text:
	list1 = list(line)
	new_line = ''
	for l in list1:
		if (l.isalpha() or l.isdigit() or l in ", .?!'@#$%&*(){}[]<>"):
			if not(l in 'âÃã²ðº³'):
				new_line += l
	new_text += new_line + '\n' 

#print(new_text)
LetterCount(new_text)

op = open("RAW_bars.txt",'w+')
op.write(new_text)
op.close()

f.close()
sl.close()



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
