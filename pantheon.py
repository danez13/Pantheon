import argparse
import validators
import urllib.parse
import logging
from MODULES.infoGathering import scraper

logging.basicConfig(filename="LoggingData/pantheon_main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

logger = logging.getLogger()

logger.setLevel(logging.NOTSET)

if __name__ == "__main__":

    logger.info("logging main module has started")
    
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
    logger.debug(f"IP validation [{user_input}]")
    ipBool = False
    if validators.ip_address.ipv4(user_input):
        ipBool = True
        ip = user_input
    else:
        logger.warning(f"[{user_input}] is not a IP")

    url = user_input
    parts = urllib.parse.urlsplit(url)
    
    # check if scheme is present
    if parts.scheme == "":
        url = "https://" + url

    # check if valid domain
    logger.debug(f"IP validating [{user_input}]")
    domainBool = False
    if validators.domain(parts.hostname):
        domainBool = True
    else:
        logger.warning(f"[{user_input}] is not a domain")

    if not domainBool and not ipBool:
        logger.error(f"[{user_input}] is not a domain or IP")

    # if a domain do the following:
    if domainBool:
        logger.debug(f"scraping [{parts.geturl()}] for info")
        # scrape for sub-urls
        scraper.scrape(parts.geturl(),limit,fileStoreBool,siteMapBool,advanceSearch,emailBool)

    