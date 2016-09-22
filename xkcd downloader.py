import os,requests as req,bs4

print "Downloading the xkcd comics...."

url = 'http://xkcd.com/'
if not os.path.exists('xkcd'):
	os.makedirs('xkcd')

while not url.endswith('#'):
	
	#response from the server
	try:
		print("URL: %s"%(url))
		res = req.get(url)
		res.raise_for_status()
	except Exception as e:
		print("URL: %s"%(url))
		print e
		print "Aborting as server could not be connected"
		break

	soup = bs4.BeautifulSoup(res.text,"html.parser")

	#image
	imageurl = soup.select('#comic > img')
	if imageurl == []:
		print "Could now find comic element"
	else:
		try:
			impath = imageurl[0].get('src')
			img = req.get('http:'+impath)
			img.raise_for_status()
		except:#incase image cant be loaded...
			# skip this image...
			previousurl = soup.select('a[rel="prev"]')[0]
			url = 'http://xkcd.com'+previousurl.get('href')
			continue
		#saving the image
		with open(os.path.join('xkcd',os.path.basename(impath)),'wb') as imagefile:
			for chunk in img.iter_content(100000):
				imagefile.write(chunk)

	print "DONEEEE"
	#url to the previous comic
	previousurl = soup.select('a[rel="prev"]')[0]
	url = 'http://xkcd.com'+previousurl.get('href')

print "Done saving all the files"