import requests
import urllib.request
from bs4 import BeautifulSoup
import os.path
from os import path
import time
import random
import sys



#header={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3","Accept-Encoding": "gzip,deflate, br","Accept-Language": "en-US,en;q=0.9", "Host":"https://www.azlyrics.com" , "Referer": "https://www.google.com/","Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0 ",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 ",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate",
"Referer": "https://www.google.com/",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests" : "1" }


#print(len(sys.argv))
if not(len(sys.argv) == 2):
	print("i need how many computers are you using")
	exit()

num_pcs = int(sys.argv[1])
#gonna pull a sneky acet116-lnx-1.bucknell.edu
myhostnum = int(os.uname()[1].split('-')[2].split('.')[0]) % num_pcs #possibly % num machines i will use machines 1 to 9 so im not worried
print(myhostnum)

url = '!i' #not null

#need number of computers
song_lines = list()
song_urls = list()


song_list = open("song_list.txt", 'r')
song_lines = song_list.read().split('\n')
song_list.close()
song_lines.remove('')
song_url = open("url_list.txt","r")
song_urls = song_url.read().split('\n')
song_url.close()
song_urls.remove('')


total_lines = len(song_lines) -1
#i will use computers 1 to 9 from the brki lab 

#song_lines now has all the songs
#num_lines has how many lyrics each will get


while not(total_lines == -1):
	if(total_lines%num_pcs == myhostnum):#if the song should be delt with by my host 
		url = song_urls[total_lines]
		fname = song_lines[total_lines]
		fname = fname.rstrip()# strip the \n
		fname = fname + '.txt'
		url = url.rstrip()
		total_lines -= 1
		if(path.exists('lyrics/' + fname)):# if my lyrics file already exists dont remake it
			continue # should continue the while re checking first if


#		delay before trying to get url
		delay = random.uniform(10,20) #sleep for 10 to 20 seconds to avoid ipban? it knows that something is pinging it in underseonds
		print(url)
		print('time delay = ' + str(delay))
		#print('urls remaining: ' + str(num_lines)) 
		time.sleep(delay)
		
		try:
			r = requests.get(url, headers=header)
		except:
			print("THEY FOUND ME IM BURNED: " + os.uname()[1])
			print("BAD URL: " + url) #they keep ip banning me
			exit()	
	
		if len(url) == 0: #if eof break
			break
		print('WORKED-------------------------------------------------------------------------------------------------')

		
		soup = BeautifulSoup(r.text, 'html.parser')
		#print(soup)
		
		song_lyrics = open("lyrics/" + fname,"w+", encoding = "utf-8") #new lyrics file 
		results = soup.find_all('div', attrs={'class':'col-xs-12 col-lg-8 text-center'})
		lis = str(results).split('\n')
		hit = False
		for line in lis:	
			if('<!-- MxM banner -->' in line):
				break
			if(hit):
				song_lyrics.write(line + '\n') #write lyrics to song_lyric file
			if('Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that'in line):
				hit = True
		song_lyrics.close()
	total_lines-=1
print("wow i finished")

