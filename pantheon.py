from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import argparse

scraped_urls = set()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 
siteMap = {}
if __name__ == "__main__":
    # processing command line arguements
    parser = argparse.ArgumentParser(
                    prog='Pantheon',
                    description='all in one basic hacking tool',
                    epilog='HI ;)')
    parser.add_argument("url", help="input-url")
    parser.add_argument("-l","--limit",help="url-limit",default=-1,type=int,dest="limit")
    parser.add_argument("-S", "--SQL",help="implement SQL injection on any queries found", action="store_true",dest="sqlBool")
    
    # add arguements to local variables
    args = parser.parse_args()
    user_url=args.url
    limit = args.limit
    SQLBool= args.sqlBool
    
    # initialize necessary variables
    urls = deque([user_url])
    count = 0
    parts = urllib.parse.urlsplit(user_url)
    file = open("Files/"+parts.hostname,"w")
    while len(urls):

        # check if limit has been reached
        if count == limit:
            break
        # manage collections
        url = urls.popleft()
        scraped_urls.add(url)

        # intialize site map population
        siteMap["site"] = url
        siteMap["Children"] = {}
        siteMap["query"] = []

        # parse current url
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
        
        # populate site map
        # subPaths = parts.path[1:]
        # if subPaths != "":
        #     subPaths=subPaths.split("/")
        #     for index,subPath in enumerate(subPaths):
        #         if index == 0 and not subPath in siteMap["Children"]:
        #             siteMap["Children"][subPath]["site"] = 
        # add found queries
        # if parts.query != "":
            # siteMap["query"].append("?"+parts.query)
        
        # check if current url is a sub-url of the user input url
        if path.find(user_url) == -1:
            continue
        
        # print('[%d] Processing %s' % (count, url))
        # file.write(url+"\n")

        # request html response fron the page
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
        count += 1
    file.close()

    