from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import json
import os
import re
import logging
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' } 

logging.basicConfig(filename="LoggingData/pantheon_main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

logger = logging.getLogger()

logger.setLevel(logging.NOTSET)

def __populateSiteMap(siteMap:dict,parts:urllib.parse.SplitResult,FileBool:bool):
    # get hostname concatenated with hostname
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
                # create template
                temp={
                    "site":base_url + tempPath,
                    "Children":{},
                    "query":[]
                }

                # check if the link has a query
                if index == len(subPages)-1 and parts.query != "":
                    temp["query"].append("?"+parts.query)

                tempMap["Children"][subPage]=temp
            tempMap = tempMap["Children"][subPage]
    #  if FileBool is True: open siteMap file to store SiteMap
    if FileBool:
        with open(f"Files/{parts.hostname}/Map.json","w+") as outfile:
            logger.debug(f"creating File for storing site map: {outfile}")
            json.dump(siteMap,outfile)
    return siteMap

def scrape(input_url:str, limit:int, FileBool:bool,siteMapBool:bool,advSearchBool:bool, emailBool:bool):
    logger.info("scrape logging has started")
    urls = deque([input_url])

    scraped_urls = set()
    count = 0

    # if emailBool is True: create website directory
    if emailBool:
        emails = set()

    # if urlFileBool is True: create file to store urls
    if FileBool:
        parts = urllib.parse.urlsplit(input_url)
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

            # if urlFileBool is True: Write urls to file
            if FileBool:
                logger.debug(f"writing to {urlFile}")
                urlFile.write(url+"\n")
            else:
                # if count is less than true or advanceSearchBool is True: print out processing url else print out url found
                if count < limit or advSearchBool:
                    print('[%d] Processing %s' % (count, url))
                else:
                    print("[%d] Found %s" % (count, url))

            # if siteMapBool is True: populate sitemap
            if siteMapBool:
                siteMap = __populateSiteMap(siteMap,parts,FileBool)

            # if count < limit or advSearchBool is True:
            if count < limit or advSearchBool:
                time.sleep(3)
                try:
                    logger.debug(f"request [{parts.hostname}] HTML page")
                    response = requests.get(url,headers=headers)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as error:
                    logger.error(error)
                    continue

                # if emailBool is True: scrape for new emails
                if emailBool:
                    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
                    emails.update(new_emails)

                logger.debug("creating html parser")
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

    # if emailBool True: collect emails and print
    if emailBool:
        # if FileBool is True: open file to save gathered emails to
        if FileBool:
            logger.debug(f"opening [Files/{parts.hostname}/email.txt] for writing")
            emailFile = open(f"Files/{parts.hostname}/email.txt","w")
        for mail in emails:
            # if FileBool is True: write gathered emails to file
            if FileBool:
                logger.debug(f"writing to {emailFile}")
                emailFile.write(mail)
            else:
                print(mail)
    
    # if FileBool is True: close file used to store urls
    if FileBool:
        urlFile.close()