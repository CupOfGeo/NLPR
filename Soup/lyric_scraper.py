import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
from os import path
#import itemListElementfrom bs4 import BeautifulSoup



#url = 'https://www.azlyrics.com/lyrics/kendricklamar/maadcity.html'
#url2 = 'https://www.azlyrics.com/lyrics/kendricklamar/bitchdontkillmyvibe.html'
#url3 = 'https://www.azlyrics.com/lyrics/kendricklamar/backseatfreestyle.html'
url ="https://www.azlyrics.com/lyrics/eminem/drips.html"
'''
url = '!i'
song_list = open("song_list.txt", 'r')
idx = 0

with open("url_list.txt", "r") as song_url:
	while(len(url) > 1):
		url = song_url.readline()
		fname = song_list.readline()
		fname = fname.rstrip()# strip the \n
		fname = fname + '.txt'
		url = url.rstrip()
		while (path.exists('lyrics/' + fname)):# if my lyrics file already exists dont remake it also check url status code to be working
			url = song_url.readline()
			fname = song_list.readline()
			fname = fname.rstrip()# strip the \n
			fname = fname + '.txt'
			url = url.rstrip()
'''

try:
	r = requests.get(url)
except:
	print("BAD URL: " + url)
	exit()#continue	
	
#if len(url) == 0: #if eof break
#	break

print(url)# works
		#url = url.rstrip()
		#if requests.get(url) != 200:
			#ye fucked up
		
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup)
		#song_lyrics = open("lyrics/" + fname,"w+") #new lyrics file 
results = soup.find_all('div', attrs={'class':'col-xs-12 col-lg-8 text-center'})

lis = str(results).split('\n')
bo = False
for line in lis:
	if line.startswith('<!-- MxM banner -->'):
		break
	if(bo):
		print(line)
	if line.startswith('<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'):
		bo = True
#song_list.close()
#song_url.close()
#:wq
#song_list.close()
