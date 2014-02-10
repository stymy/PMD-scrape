import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup

PMID = 22659001

def find_pdflink(soup):
    for action in soup.find_all("a"):
        link = action.get('href')
        try: is_pdf=link[-4:]==".pdf"
        except TypeError:continue
        if is_pdf: 
            return link
        
def get_cookie():
    cj = cookielib.CookieJar()
    cookieopener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    formdata = { "sso_user" : "aw2555", "sso_pass": "EK7XfY94Ma"}
    encodedform = urllib.urlencode(formdata)
    cookie_response = cookieopener.open("https://library.med.nyu.edu/cgi-bin/sso.pl", encodedform)
    if cookie_response.msg == "OK":
        return cj
    else:
        print "Login Failed"

cookie_handler= urllib2.HTTPCookieProcessor(get_cookie())
redirect_handler= urllib2.HTTPRedirectHandler()
opener = urllib2.build_opener(redirect_handler,cookie_handler)

my_headers = {
'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
'Accept-Language': 'en-gb,en;q=0.5',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
'Connection': 'keep-alive'
}
req_url = urllib2.Request('http://www.pubget.com/pdf/'+str(PMID),headers=my_headers)
response_url = opener.open(req_url)
data = response_url.read()
if response_url.url[-4:]!=".pdf":
    req_file = urllib2.Request('http://ezproxy.med.nyu.edu/login?url='+response_url.url,headers=my_headers)
    response_file = opener.open(req_file)
    open("/home/rschadmin/Cache/"+str(PMID), 'w').write(data) #save cache
    soup = BeautifulSoup(data)
    pdflink = find_pdflink(soup)
    req_file_again = urllib2.Request(pdflink,headers=my_headers)
    response_file_two = opener.open(req_file_again)
    data = response_file_two.read()
with open ("/home/rschadmin/Data/scraped/"+str(PMID)+".pdf","wb") as savepdf:
    savepdf.write(data)
