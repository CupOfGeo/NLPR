'''
song_list_url scraper
uses the artists.txt to create song_list.txt and url_lsit.txt
'''
import requests
from bs4 import BeautifulSoup
import time
import random
from os import path

fname = ''
while not(path.exists(fname)):
	fname = input("folder name?")


out = open(fname + "/song_list.txt", "w+")
outurls = open(fname + "/url_list.txt", "w+")

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0 ",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 ",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate",
"Referer": "https://www.google.com/",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests" : "1" }


with open(fname + "/artists.txt", "r") as f:
	line = f.readline() #first line is ARTISTS:
	while(True):
		url = 'https://www.azlyrics.com/' #base url 
		line = f.readline()
		while (line.startswith('//')): # if commented out read next line
			line = f.readline()
		if len(line) == 0: #if eof break
			break

		artist = line #artist name from file
		line = line.replace(' ','')
		line = line.rstrip() #formating
		if line[0].isnumeric():# I <3 50 cent woundt be a rap ai with him
			url = url + '19/' + line + '.html'
		else:
			url = url + line[0] + '/' + line + '.html'

		result = requests.get(url, headers=header) # request html
		delay = random.uniform(7,13) #sleep for 7 to 13 seconds to avoid ipban? it knows that something is pinging it in underseonds
		print(url)
		print('time delay = ' + str(delay))
		time.sleep(delay)
		src = result.content
		soup = BeautifulSoup(src, 'lxml')

		songs = []
		for a_tag in soup.find_all('a'):
			ext = a_tag.get('href') # all links look like ../lyrics/<artists>/<song>.html
			#print(ext)
			#print(line)
			if(ext == None):
				continue	
			if (line in ext) and ('..' in ext):
				song_name = ext.split('/')[3].split('.')[0]
				if not(song_name in songs) and not('skit' in song_name) and not('interlude' in song_name):
				 #dont get repeats and skits / interludes
					songs.append(song_name)
					out.write(ext.split('/')[2] + "_" + song_name + '\n') #artist_song
					ext = ext.strip('..')
					outurls.write('https://www.azlyrics.com/' + ext + '\n') 

			
#print(urls)
f.close()
out.close()
outurls.close()
