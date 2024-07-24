import argparse
import validators
import urllib.parse
import logging
from MODULES.informationGathering import scraper,domainLookup

logging.basicConfig(filename="LoggingData/pantheon_main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

logger = logging.getLogger()

logger.setLevel(logging.NOTSET)

if __name__ == "__main__":

    logger.info("logging main module has started")
    
    # processing command line arguements
    parser = argparse.ArgumentParser()
    
    # main arguements
    parser.add_argument('host', help='Host name or IP address')

    # create subparsers
    subparsers = parser.add_subparsers(dest='cmd', title='subcommands')

    # scraper subParser
    scrapeParser = subparsers.add_parser('scrape', help='Scrape a website')
    scrapeParser.add_argument('-l',"--limit",type=int,default=1, help='Limit value',dest="limit")
    scrapeParser.add_argument("-fs","--FileStore",help="store to file",action="store_true",dest="fileStoreBool")
    scrapeParser.add_argument("-sm","--SiteMap",help="create site map",action="store_true",dest="siteMapBool")
    scrapeParser.add_argument("-as","--advSearch",help="advance search",action="store_true",dest="advSearchBool")
    scrapeParser.add_argument("-es","--emailSearch",help="search for emails",action="store_true",dest="emailBool")

    # domain look up subParser
    domainLookUpParser = subparsers.add_parser("domainLookup", help="look up domain information")
    domainLookUpParser.add_argument("-fs","--FileStore",help="store to file",action="store_true",dest="fileStoreBool")
    domainLookUpParser.add_argument("-fO","--FormatDomain",help="format domain look up output",action="store_true",dest="formatDomainBool")

    # add arguements to local variables
    args = parser.parse_args()
    user_input=args.host
    cmd = args.cmd
    if cmd == "scrape":
        limit = args.limit
        fileStoreBool = args.fileStoreBool
        siteMapBool = args.siteMapBool
        advSearchBool = args.advSearchBool
        emailBool = args.emailBool
    if cmd == "domainLookup":
        fileStoreBool = args.fileStoreBool
        formatDomainBool = args.formatDomainBool

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
        parts = urllib.parse.urlsplit(url)

    # check if valid domain
    logger.debug(f"IP validating [{user_input}]")
    domainBool = False
    if validators.domain(parts.hostname):
        domainBool = True
    else:
        logger.warning(f"[{user_input}] is not a domain")

    if not domainBool and not ipBool:
        logger.error(f"[{user_input}] is not a domain or IP")
        print(f"{user_input} is neither a domain or IP")
        exit()

    # if a domain do the following:
    if domainBool:
        # scrape url
        if cmd == "scrape":
            logger.debug(f"scraping [{parts.geturl()}] for info")
            # scrape for sub-urls
            scraper.scrape(parts.geturl(),limit,fileStoreBool,siteMapBool,advSearchBool,emailBool)
        # domain lookup on url
        if cmd == "domainLookup":
            logger.debug(f"looking up {parts.geturl()} domain info")
            domain_info = domainLookup.getDomainInfo(parts.hostname,fileStoreBool)
            # if formatDomainBool is True: format domain lookup info else print unformatted info
            if formatDomainBool:
                domainLookup.formatDomainInfo(domain_info,(parts.hostname,fileStoreBool))
            else:
                print("Domain INFO:")
                print(domain_info)


    