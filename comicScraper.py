#! python3 # comicScraper.py - Scrape web comics for comic images.

# This script is based off of the xkcd scraper in Automate The Boring Stuff by Al Sweigart
# I've extended it a little to make work for a few of my favourite webcomics and pulled
# some of the code into functions to make it easier to add more comics in future.

import requests, os, bs4, urllib3


def getComics(baseUrl, startUrl, dirName, comicElemStr, prevLinkStr):
	url = startUrl

	for i in range(100):
		print('Downloading page %s...' % url)
		res = requests.get(url)
		try:
			res.raise_for_status()
		except:
			res = requests.get(url)
			res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, "html5lib")

		# Find the URL of the comic image.
		comicElem = soup.select(comicElemStr)

		if comicElem == []:
			print('Could not find comic image.')
		else:
			if comicElem[0].get('src').startswith('http'):
				comicUrl = comicElem[0].get('src')
			else:
				comicUrl = "http:" + comicElem[0].get('src')
			# Download the image.
			print('Downloading image %s...' % (comicUrl))
			try:
				res = requests.get(comicUrl)
			except urllib3.exceptions.LocationParseError as e:
				print('couldn\'t download ' + comicUrl)
				print(e)
				prev = soup.select(prevLinkStr)[0]
				url = baseUrl + prev.get('href')
				continue
			except requests.exceptions.Timeout as e:
				print('couldn\'t download ' + comicUrl)
				print(e)
				prev = soup.select(prevLinkStr)[0]
				url = baseUrl + prev.get('href')
				continue
			except requests.exceptions.TooManyRedirects as e:
				print('couldn\'t download ' + comicUrl)
				print(e)
				prev = soup.select(prevLinkStr)[0]
				url = baseUrl + prev.get('href')
				continue
			except requests.exceptions.RequestException as e:
				print('couldn\'t download ' + comicUrl)
				print(e)
				prev = soup.select(prevLinkStr)[0]
				url = baseUrl + prev.get('href')
				continue

			res.raise_for_status()

			# Save to dir.
			file = open(os.path.join(dirName, str(i)+'.png'), 'wb')
			for chunk in res.iter_content(100000):
				file.write(chunk)
				file.close()

		prev = soup.select(prevLinkStr)[0]
		if prev.get('href').startswith('http'):
			url = prev.get('href')
		else:
			url = baseUrl + prev.get('href')
		i += 1
	return

baseDirName = 'comics/'

#XKCD
startUrl = 'http://xkcd.com'	# url to start crawling from
baseUrl = startUrl # base URL of the site for relative links
dirName = baseDirName+'xkcd'
comicElemStr = '#comic img'
prevLinkStr = 'a[rel="prev"]'

os.makedirs(dirName, exist_ok=True)	# store comics in ./xkcd

getComics(baseUrl, startUrl, dirName, comicElemStr, prevLinkStr)

print('XKCD Done.')


#Cyanide and Happiness
startUrl = 'http://explosm.net/comics/latest'	# url to start crawling from
baseUrl = 'http://explosm.net/' # base URL of the site for relative links
dirName = baseDirName+'cyanide-and-happiness'
comicElemStr = 'img#main-comic'
prevLinkStr = 'a.previous-comic'

os.makedirs(dirName, exist_ok=True)	# store comics in ./cyanide-and-happiness

getComics(baseUrl, startUrl, dirName, comicElemStr, prevLinkStr)

print('C&H Done.')


#Dinosaur Comics
startUrl = 'http://www.qwantz.com/'	# url to start crawling from
baseUrl = startUrl # base URL of the site for relative links
dirName = baseDirName+'dinosaur-comics'
comicElemStr = 'img.comic'
prevLinkStr = 'a[rel="prev"]'

os.makedirs(dirName, exist_ok=True)	# store comics in ./dinosaur-comics

getComics(baseUrl, startUrl, dirName, comicElemStr, prevLinkStr)

print('Dinosaur Comics Done.')


