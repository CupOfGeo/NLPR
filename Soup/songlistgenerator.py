'''
song_list_url scraper
'''
import requests
from bs4 import BeautifulSoup
import time

out = open("song_list.txt", "w+")
outurls = open("url_list.txt", "w+")

with open("artists.txt", "r") as f:
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

		result = requests.get(url) # request html
		time.sleep(random.uniform(7,13) #sleep for 7 to 13 seconds to avoid ipban? it knows that something is pinging it in underseonds
		src = result.content
		soup = BeautifulSoup(src, 'lxml')

		songs = []
		for a_tag in soup.find_all('a'):
			#urls.append(
			ext = a_tag.get('href') # all links look like ../lyrics/<artists>/<song>.html
			if (line in ext) and ('..' in ext):
				out.write(ext.split('/')[2] + "_" + ext.split('/')[3].split('.')[0] + '\n') #artist_song
				ext = ext.strip('..')
				outurls.write('https://www.azlyrics.com/' + ext + '\n') 

#print(urls)
f.close()
out.close()
outurls.close()
