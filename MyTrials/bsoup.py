import bs4 
import urllib.request
import clipboard


url="http://www.google.com/?#q=ballon"
url2="http://arstechnica.com"
key='ballon'
sauce= urllib.request.urlopen(url).read()
soup=bs4.BeautifulSoup(sauce)

#print(soup.find_all('p'))
#print(soup)
for paragragh in soup.find_all('p'):
	print(paragragh.text)
	
#images = soup.find_all('p')

#urllib.request.urlretrieve('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfuKgKdcB8EH6xXBng73z3o31CbKuEB1AcFOwImysr4QWUl8yYUtD83uD3','test.jpg')
#print(images.text)

urllib.request.urlretrieve(clipboard.get(),'test.jpg')
