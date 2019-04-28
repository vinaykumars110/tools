import webbrowser
import urllib.request
import random
import clipboard
from bs4 import BeautifulSoup


new=2

def download_image(url):
	img_name=random.randrange(1,10)
	full_name=str(img_name)+'.jpg'
	urllib.request.urlretrieve(url,full_name)
	
	
#url3="https://lh3.googleusercontent.com/proxy/y806ZdwUvj_ryStQe5LKNzzb8P-IXfb53VcUKJONHW90B81b1ZiUYeerI-APFWiBX1PCNFiJV2QN_cfzN_YVYDOqpEi4jJY=w292-h503-nc"

taburl="http://www.google.com/?#q="
url="http://www.images.google.com/?#q="
#term= raw_input("Enter search query: ")
term='vocabulary'
webbrowser.open(taburl+term)
#webbrowser.open(url3)

websitecode=urllib.request.urlopen("http://arstechnica.com").read()
print(websitecode)
sp=BeautifulSoup(websitecode)

images=sp.findAll('img')
print(images)
