import urllib2

PMID = 	18083565

opener = urllib2.build_opener()
my_headers = {
'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-GB; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
'Accept': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
'Accept-Language': 'en-gb,en;q=0.5',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
'Connection': 'keep-alive'
}
req = urllib2.Request('http://www.pubget.com/pdf/'+str(PMID),headers=my_headers)
response = opener.open(req)
data = response.read()
with open ("/home/rschadmin/Data/scraped/"+str(PMID)+".pdf","wb") as pdf:
    pdf.write(data)
