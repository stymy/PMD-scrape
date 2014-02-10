import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup

PMID = 	18083565

def return_pdf(link):
    if :
        return link

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

req_file = urllib2.Request('http://ezproxy.med.nyu.edu/login?url='+response_url.url,headers=my_headers)
response_file = opener.open(req_file)
data = response_file.read()
if response_file.url[-4:]!=".pdf":
    open("/home/rschadmin/Cache/"+str(PMID), 'w').write(data) #save cache
    data = response_file.read()
    soup = BeautifulSoup(data)
    for action in soup.find_all("a"):
        link = action.get('href')
        if link:
            if link[-4:]==pdf
                req_file = urllib2.Request('http://ezproxy.med.nyu.edu/login?url='+response_url.url,headers=my_headers)
with open ("/home/rschadmin/Data/scraped/"+str(PMID)+".pdf","wb") as pdf:
    pdf.write(data)
