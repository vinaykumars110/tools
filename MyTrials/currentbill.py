import urllib.request
import re

url="http://bescom.org/en/pay-bill/"
url2="https://www.bescom.co.in/SCP/MyAccount/QuickPayment.aspx?AccountID=8928945000"
url3="https://www.bescom.co.in/"
html=urllib.request.urlopen(url2)
html=html.read()
print(str(html))


