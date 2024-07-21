import argparse
import validators
import urllib.parse
import logging
from MODULES.infoGathering import scraper

logging.basicConfig(filename="LoggingData/pantheon-main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

# create loggin object
logger = logging.getLogger()

# setting the logger threshhold to DEBUG
logger.setLevel(logging.CRITICAL)

logger.info("Main logging has been Started")

if __name__ == "__main__":
    
    # processing command line arguements
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="host url",type=str)
    parser.add_argument("-l","--limit",help="limit search",type=int,default=1,dest="limit")
    parser.add_argument("-fs","--FileStore",help="store to file",action="store_true",dest="fileStoreBool")
    parser.add_argument("-sm","--SiteMap",help="create site map",action="store_true",dest="siteMapBool")
    parser.add_argument("-as","--advSearch",help="advance search",action="store_true",dest="advanceSearch")
    parser.add_argument("-es","--emaailSearch",help="search for emails",action="store_true",dest="emailBool")
    
    # add arguements to local variables
    args = parser.parse_args()
    user_input=args.host
    limit = args.limit
    fileStoreBool = args.fileStoreBool
    siteMapBool = args.siteMapBool
    advanceSearch = args.advanceSearch
    emailBool = args.emailBool

    # check if IP address
    ipBool = False
    logger.debug(f"IP validation of [{user_input}]")
    if validators.ip_address.ipv4(user_input):
        ipBool = True
        ip = user_input

    url = user_input
    parts = urllib.parse.urlsplit(url)
    
    # check if scheme is present
    if parts.scheme == "":
        url = "https://" + url

    # check if valid domain
    domainBool = False
    logger.debug(f"domain validation of [{user_input}]")
    if validators.domain(parts.hostname):
        domainBool = True

    if not domainBool and not ipBool:
        logger.error(f"{user_input} is not a domain or an ip")

    # if a domain do the following:
    if domainBool:
        logger.debug(f"scraping [{parts.geturl()}] for info")
        # scrape for sub-urls
        scraper.scrape(parts.geturl(),limit,fileStoreBool,siteMapBool,advanceSearch,emailBool)

    
    