import urllib2
from BeautifulSoup import  BeautifulSoup
url = "http://offers.smartbuy.hdfcbank.com/offer_details/46423/cc_online_shopping1"
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
print "1/",soup.find("span", "left size18 lblue").text #title
print "2/",soup.find("span", "left size15 dark").text #text below the title 
print "3/",soup.find("span", "lred2 bold size15").text
print "5/url:",url
