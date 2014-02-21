# rmo needed to make some marginal changes for this to be importable

import urllib2
import urllib
import cookielib
from urlparse import urlparse
from bs4 import BeautifulSoup

moz_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
    'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
    'Accept-Language': 'en-gb,en;q=0.5',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Connection': 'keep-alive'
    }

def find_pdflink(soup):
    for action in soup.find_all("a"):
        link = action.get('href')
        try: is_pdf=link.endswith(".pdf")
        except AttributeError:continue
        if is_pdf:         
            return link
        else:
            try: is_pdf=str(action).find("PDF")
            except AttributeError:continue
        if is_pdf>0:
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
        #pubget or wily -> pubmed
        if response_url.url.startswith('http://pubget.com'):
            pmd_url = 'http://www.ncbi.nlm.nih.gov/pubmed/?term='+str(PMID)
            pmd_page = urllib2.urlopen(pmd_url).read()
            pmd_soup = BeautifulSoup(pmd_page)
            link_out = pmd_soup.find("div",class_="icons")
            try: pub_url = 'http://ezproxy.med.nyu.edu/login?url='+link_out.find(href=True)['href'] 
            except TypeError:
                print "There is no pdf link out of PubMed:"+pmd_url
                
        #if response_url.url.startswith('http://onlinelibrary.wiley.com'):
            #wiley_soup = BeautifulSoup(data)
            #import pdb; pdb.set_trace()
            #from zotero
            #m = wileysoup.find(id="pdfDocument")
            #if(m) {
                #m[1] = ZU.unescapeHTML(m[1]);
                #Z.debug(m[1]);
        #Science Direct
        else:
            pub_url = 'http://ezproxy.med.nyu.edu/login?url='+response_url.url
        req_pub = urllib2.Request(pub_url,headers=my_headers)
        response_pub = opener.open(req_pub)
        sd_soup = BeautifulSoup(response_pub.read())
        pdflink = find_pdflink(sd_soup)
        
        #handle relative links
        if not pdflink.startswith('http://'):
            parsed = urlparse(response_pub.url)
            pdflink = parsed.scheme+'://'+parsed.netloc+pdflink
            
        req_file = urllib2.Request(pdflink,headers=my_headers)
        response_file = opener.open(req_file)
        data = response_file.read()
    with open ("/home/rschadmin/Data/scraped/"+str(PMID)+".pdf","wb") as savepdf:
        if data.startswith('%PDF'):
            savepdf.write(data)
        else:
            with_flag= response_pub.url+'/n'+pdflink+'/n'+response_file.url+'/n'+data
            raise RuntimeError
            import pdb; pdb.set_trace()
            savepdf.write(with_flag)

def get_opener():
    cookie_handler= urllib2.HTTPCookieProcessor(get_cookie())
    redirect_handler= urllib2.HTTPRedirectHandler()
    opener = urllib2.build_opener(redirect_handler,cookie_handler)
    return opener
