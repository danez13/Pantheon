from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import argparse
import os
import time
from MODULES.SiteMap import populateSiteMap

scraped_urls = set()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
if __name__ == "__main__":
    
    # processing command line arguements
    parser = argparse.ArgumentParser(
                    prog='Pantheon',
                    description='all in one basic hacking tool',
                    epilog='HI ;)')
    parser.add_argument("url", help="input-url")
    parser.add_argument("-l","--limit",help="url-limit",default=-1,type=int,dest="limit")
    # parser.add_argument("-Si", "--SQLi",help="implement SQL injection on any queries found", action="store_true",dest="sqlBool")
    parser.add_argument("-aS", "--advSearch", help="advance search", action="store_true", dest="searchBool")

    # add arguements to local variables
    args = parser.parse_args()
    user_url=args.url
    limit = args.limit
    # SQLBool= args.sqlBool
    searchBool = args.searchBool

    # initialize necessary variables
    urls = deque([user_url])
    count = 0
    parts = urllib.parse.urlsplit(user_url)

    # create website directory
    try:  
        os.makedirs(f"Files/{parts.hostname}")  
    except OSError as error:  
        print(error)

    # create/open found urls document
    file = open(f"Files/{parts.hostname}/url.txt","w")

    # intialize site map population
    siteMap = {}
    siteMap["site"] = user_url
    siteMap["Children"] = {}
    siteMap["query"] = []

    while len(urls):

        # manage collections
        url = urls.popleft()
        scraped_urls.add(url)

        # parse current url
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # check if current url is a sub-url of the user input url
        if path.find(user_url) == -1:
            continue

        print('[%d] Processing %s' % (count, url))
        file.write(url+"\n")

        # populate siteMap
        siteMap = populateSiteMap(siteMap,parts)
        
        if count==1 and (not searchBool) and limit==-1:
            continue
        else:
            # request html response fron the pagecle
            time.sleep(3)
            try:
                response = requests.get(url,headers=headers)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            soup = BeautifulSoup(response.text,features="html.parser")

            # find all links on a webpage
            for anchor in soup.find_all("a"):
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in urls and not link in scraped_urls:
                    urls.append(link)
        
        # check if limit has been reached
        if count == limit:
            break
        
        count += 1
    file.close()

    