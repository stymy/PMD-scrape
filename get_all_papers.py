from pmd_scraper2 import get_opener, get_pdf, moz_headers

import os

OUT_PATTERN = os.path.join(os.environ["HOME"], "Data", "scraped", "%d.pdf")

# Assumes a file called PUBMED_IDS exists with one-per-line pubmed IDs
ids = [int(X) for X in open("PUBMED_IDS").read().split("\n")]

opener = get_opener()

for id in ids:
    pdf_outfile = OUT_PATTERN % (id)
    if not os.path.exists(pdf_outfile):
        # cache fail -- download
        try:
            get_pdf(id, opener, moz_headers)
        except KeyboardInterrupt:
            print 'quitting'
            break
        except:
            print 'failed to download %d' % (id)
    else:
        print "cache hit", id
