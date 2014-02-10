from bs4 import BeautifulSoup
import urllib2, urllib
import cookielib

PMID = 	18234519
cj = get_cookie()

def get_page(url,cj): #cache webpages locally
    print url
    filename = '/home/rschadmin/Cache/'+urllib2.quote(url, safe='')
    try:
        return open(filename).read()
    except IOError:    
        cookie_handler= urllib2.HTTPCookieProcessor(cj)
        redirect_handler= urllib2.HTTPRedirectHandler()
        opener = urllib2.build_opener(redirect_handler,cookie_handler)
        page = opener.open(url).read()
        open(filename, 'w').write(page)
        return page
        
def get_cookie():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    formdata = { "username" : "aw2555", "password": "EK7XfY94Ma", "form-class" : "login" }
    encodedform = urllib.urlencode(formdata)
    response = opener.open("https://library.med.nyu.edu/cgi-bin/sso.pl", encodedform)
    if response.msg == "OK":
        return cj
    else:
        print "Login Failed"
        
pmd_url = 'http://www.ncbi.nlm.nih.gov/pubmed/?term='+str(PMID)        
pmd_page = get_page(pmd_url,cj)
pmd_soup = BeautifulSoup(pmd_page)

link_out = pmd_soup.find("div",class_="icons")
nyu_url = 'http://ezproxy.med.nyu.edu/login?url='+link_out.find(href=True)['href']

pub_page = get_page(nyu_url,cj)
pub_soup = BeautifulSoup(pub_page)

my_headers = {
'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
'Accept-Language': 'en-gb,en;q=0.5',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
'Connection': 'keep-alive'
}
req = urllib2.Request('http://www.pubget.com/pdf/18234519',headers=my_headers)
response = opener.open(req)
data = response.read()
with open ("/home/rschadmin/Desktop/trydata.pdf","wb") as pdf:
    pdf.write(data)
