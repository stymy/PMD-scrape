import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup

def find_pdflink(soup):
    for action in soup.find_all("a"):
        link = action.get('href')
        try: is_pdf=link.endswith(".pdf")
        except AttributeError:continue
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

def get_pdf(PMID,opener,my_headers):
    req_url = urllib2.Request('http://www.pubget.com/pdf/'+str(PMID),headers=my_headers)
    response_url = opener.open(req_url)
    data = response_url.read()
    if not response_url.url.find(".pdf")>0:
        #pubget
        if response_url.url.startswith('http://pubget.com'):
            pmd_url = 'http://www.ncbi.nlm.nih.gov/pubmed/?term='+str(PMID)
            pmd_page = urllib2.urlopen(pmd_url).read()
            pmd_soup = BeautifulSoup(pmd_page)
            link_out = pmd_soup.find("div",class_="icons")
            try: pub_url = 'http://ezproxy.med.nyu.edu/login?url='+link_out.find(href=True)['href'] 
            except TypeError:
                raise "There is no pdf link out of PubMed:"+pmd_url
        #Science Direct
        else:
            pub_url = 'http://ezproxy.med.nyu.edu/login?url='+response_url.url
        req_pub = urllib2.Request(pub_url,headers=my_headers)
        response_pub = opener.open(req_pub)
        sd_soup = BeautifulSoup(response_pub.read())
        pdflink = find_pdflink(sd_soup)
        if not pdflink.startswith('http://'):
            pdflink = response_pub.url+pdflink
        req_file = urllib2.Request(pdflink,headers=my_headers)
        response_file = opener.open(req_file)
        data = response_file.read()
    with open ("/home/rschadmin/Data/scraped/"+str(PMID)+".pdf","wb") as savepdf:
        savepdf.write(data)
    
if __name__=='__main__':
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
