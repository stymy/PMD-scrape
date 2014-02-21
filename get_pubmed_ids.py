import urllib
import os
import re

N_ARTICLES=5000
STEP_SIZE =50
URL_PATTERN="http://ec2-54-224-192-157.compute-1.amazonaws.com/annotate/index.php?expert_name=Master&status=pending_tagging&break=%d"

# make a download cache in case the script is wonky and needs to be
# run multiple times
dl_cache = os.path.join(os.environ["HOME"], "Cache", "get_pubmed_ids")
if not os.path.exists(dl_cache):
    os.makedirs(dl_cache)

cur_idx = 0
pmids = []
while cur_idx < N_ARTICLES:
    cached_path = os.path.join(dl_cache, "cmi_ann_%d.html" % cur_idx)
    if not os.path.exists(cached_path):
        # Cache miss
        open(cached_path, 'w').write(urllib.urlopen(URL_PATTERN % cur_idx).read())

    html = open(cached_path).read()

    # Look for a line like this to find the PMIDs
    # <td width='15%' valign='top'>PMID:</td><td><a target='_blank' href='http://www.ncbi.nlm.nih.gov/pubmed/?term=21119770%5Buid%5D'>21119770</a></td>					</tr> 

    pmids.extend(re.findall(r'PMID:.*\'>(\d+)<', html))

    cur_idx += STEP_SIZE

open('PUBMID_IDS', 'w').write('\n'.join(pmids))
