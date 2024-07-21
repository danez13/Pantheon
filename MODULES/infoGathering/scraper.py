from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import json
import os
import re
import logging

logging.basicConfig(filename="LoggingData/pantheon-main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

# create loggin object
logger = logging.getLogger()
# setting the logger threshhold to DEBUG
logger.setLevel(logging.DEBUG)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 

def __populateSiteMap(siteMap:dict,parts:urllib.parse.SplitResult,FileBool:bool):
    base_url = '{0.scheme}://{0.netloc}'.format(parts)
    # populate site map
    subPages = parts.path[1:]
    if subPages != "":
        subPages=subPages.split("/")
        tempPath = ""
        tempMap = siteMap

        # loop through subPaths and map each subPage
        for index,subPage in enumerate(subPages):
            tempPath += "/" + subPage
            if subPage not in tempMap["Children"]:
                temp={
                    "site":base_url + tempPath,
                    "Children":{},
                    "query":[]
                }
                # check if the link has a query
                if index == len(subPages)-1 and parts.query != "":
                    temp["query"].append("?"+parts.query)
                print(f"query: ?{parts.query}")
                tempMap["Children"][subPage]=temp
            tempMap = tempMap["Children"][subPage]
    if FileBool:
        with open(f"Files/{parts.hostname}/Map.json","w+") as outfile:
            json.dump(siteMap,outfile)
    return siteMap

def scrape(input_url:str, limit:int, FileBool:bool,siteMapBool:bool,advanceSearch:bool, emailBool:bool):
    logger.info("scrape logging has started")
    urls = deque([input_url])

    scraped_urls = set()
    count = 0

    # if urlFileBool or siteMapBool is True: create website directory
    if FileBool or siteMapBool:
        parts = urllib.parse.urlsplit(input_url)
        logger.debug(f"creating file Folder for [{parts.hostname}]")
        try:  
            os.makedirs(f"Files/{parts.hostname}")  
        except OSError as error:  
            logger.warning(error)

    # if emailBool is True: create website directory
    if emailBool:
        emails = set()

    # if urlFileBool is True: create file to store urls
    if FileBool:
        logger.debug(f"creating [Files/{parts.hostname}/url.txt] for storing urls")
        urlFile = open(f"Files/{parts.hostname}/url.txt","w")

    # if siteMapBool is True: create siteMap
    if siteMapBool:
        siteMap = {}
        siteMap["site"] = input_url
        siteMap["Children"] = {}
        siteMap["query"] = []

    try:
        while len(urls):

            url = urls.popleft()
            scraped_urls.add(url)

            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url

            # check if current url is a sub-url of the user input url
            if path.find(input_url) == -1:
                continue
            
            if count < limit or advanceSearch:
                print('[%d] Processing %s' % (count, url))
            else:
                print("[%d] Found %s" % (count, url))

            # if urlFileBool is True: Write urls to file
            if FileBool:
                logger.debug(f"writing to [Files/{parts.hostname}/url.txt]")
                urlFile.write(url+"\n")

            # if siteMapBool is True: populate sitemap
            if siteMapBool:
                siteMap = __populateSiteMap(siteMap,parts,FileBool)

            if count < limit or advanceSearch:
                try:
                    response = requests.get(url,headers=headers)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                    continue

                # if emailBool is True:
                if emailBool:
                    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
                    emails.update(new_emails)

                soup = BeautifulSoup(response.text, features="html.parser")

                for anchor in soup.find_all("a"):
                    link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                    if link.startswith('/'):
                        link = base_url + link
                    elif not link.startswith('http'):
                        link = path + link
                    if not link in urls and not link in scraped_urls:
                        urls.append(link)
            count += 1
    except KeyboardInterrupt:
        logger.warning(f"Closing due to {KeyboardInterrupt}")
        print('[-] Closing!')

    if emailBool:
        if FileBool:
            logger.debug(f"opening [Files/{parts.hostname}/email.txt] for writing")
            emailFile = open(f"Files/{parts.hostname}/email.txt","w")
        for mail in emails:
            if FileBool:
                logger.debug("writing to [Files/{parts.hostname}/email.txt]")
                emailFile.write(mail)
            print(mail)

    if FileBool:
        urlFile.close()