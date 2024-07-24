import whois
import datetime
import validators
import logging
import json
import os

logging.basicConfig(filename="LoggingData/pantheon_main.log",
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    filemode="w")

logger = logging.getLogger()

logger.setLevel(logging.NOTSET)

def getDomainInfo(host:str, fileStoreBool:bool) -> dict:
    logger.info("starting domain lookup")
    logger.debug(f"validating {'http://'+host} to be a valid domain")
    if validators.domain(host):
        try:
            logger.debug(f"looking up {'http://'+host} domain info")
            dm_info = whois.whois(host)
        except whois.parser.PywhoisError as error:
            logger.error(f"domain lookup failed for {'http://'+host}: {error}")
            raise error
        if type(dm_info) is None:
            logger.warning(f"domain lookup cameback as {None}")
            raise AttributeError
        if fileStoreBool:
            logger.debug(f"creating file Folder for [{host}]")
            try:  
                os.makedirs(f"Files/{host}")  
            except OSError as error:  
                logger.warning(error)

            logger.debug(f"creating file for writing [Files/{host}/domainInfo]")
            with open(f"Files/{host}/domainInfo.json","w+") as outfile:
                newdm_info = {}
                for key,value in dict(dm_info).items():
                    if type(value) == datetime.datetime:
                        time = value.strftime('%m/%d/%Y at %H:%M:%S')
                        newdm_info[key]=time
                    elif type(value) == list:
                        tempList = []
                        for subValue in value:
                            if type(subValue) == datetime.datetime:
                                time = subValue.strftime('%m/%d/%Y at %H:%M:%S')
                                tempList.append(time)
                            else:
                                continue
                        if len(tempList)==0:
                            newdm_info[key]=value
                        else:
                            newdm_info[key]=tempList 
                    else:
                        newdm_info[key]=value
                logger.debug(f"writing raw domain info to {outfile}")
                json.dump(newdm_info,outfile)
        return dm_info
    return {}

def formatDomainInfo(info:dict,domainFilestore:tuple):
    tp = 0
    logger.debug(f"creating file for writing [Files/{domainFilestore[0]}/formatDomainInfo.txt]")
    if domainFilestore[1]:
        outfile=open(f"Files/{domainFilestore[0]}/formatDomainInfo.txt","w+")
    for key,value in info.items():
        if value == None:
            tp = 0
            print(f"{key}: {"None".rjust(32+4-len(key)-2," ")}")
            logger.debug(f"writing formatted domain info to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}: {"None".rjust(32+4-len(key)-2," ")}\n")
        elif type(value) == datetime.datetime:
            tp = 1
            time = value.strftime('%m/%d/%Y at %H:%M:%S')
            print(f"{key}: {time.rjust(32+len(time)-len(key)-2," ")}")
            logger.debug(f"writing formatted domain info to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}: {time.rjust(32+len(time)-len(key)-2," ")}\n")
        elif type(value) == list:
            if tp == 1 or tp == 0 or tp == 3:
                print("")
                logger.debug(f"writing seperators to {outfile}")
                if domainFilestore[1]:
                    outfile.write("\n")
            tp = 2
            print(f"{key}:\n")
            logger.debug(f"writing seperators to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}:\n")
            for subValue in value:
                if type(subValue) == datetime.datetime:
                    time = subValue.strftime('%m/%d/%Y at %H:%M:%S')
                    print(f"{time.rjust(32+len(time)," ")}")
                    logger.debug(f"writing formatted domain info to {outfile}")
                    if domainFilestore[1]:
                        outfile.write(f"{time.rjust(32+len(time)," ")}\n")
                else:
                    print(f"{subValue.rjust(32+len(subValue)," ")}")
                    logger.debug(f"writing formatted domain info to {outfile}")
                    if domainFilestore[1]:
                        outfile.write(f"{subValue.rjust(32+len(subValue)," ")}\n")
            print("")
            logger.debug(f"writing seperators to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"\n")
        else:
            tp = 3
            print(f"{key}: {value.rjust(32+len(value)-len(key)-2," ")}")
            logger.debug(f"writing formatted domain info to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}: {value.rjust(32+len(value)-len(key)-2," ")}\n")
    outfile.close()