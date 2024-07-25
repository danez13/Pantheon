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
    
    # validate that the host is a domain
    if validators.domain(host):
        # get whois information about the host
        try:
            logger.debug(f"looking up {'http://'+host} domain info")
            dm_info = whois.whois(host)
        except whois.parser.PywhoisError as error:
            logger.error(f"domain lookup failed for {'http://'+host}: {error}")
            raise error
        
        # if who is information is None: raise error
        if type(dm_info) is None:
            logger.warning(f"domain lookup cameback as {None}")
            raise AttributeError
        
        # if fileStoreBool is True: open file in folder for domain
        if fileStoreBool:
            logger.debug(f"creating file for writing [Files/{host}/domainInfo]")
            with open(f"Files/{host}/domainInfo.json","w+") as outfile:
                # new dictionary to parse data inorder to format accordingly
                newdm_info = {}
                for key,value in dict(dm_info).items():
                    # if value tpye is datetime then format datetime 
                    if type(value) == datetime.datetime:
                        time = value.strftime('%m/%d/%Y at %H:%M:%S')
                        newdm_info[key]=time
                    # if value type is a list: loop through list check if datetime: format accordingly else continue
                    elif type(value) == list:
                        # create temp list for formatting
                        tempList = []
                        for subValue in value:
                            
                            # if subValue is datetime format and add to list
                            if type(subValue) == datetime.datetime:
                                time = subValue.strftime('%m/%d/%Y at %H:%M:%S')
                                tempList.append(time)
                            else:
                                continue

                        # if length of templist is 0 then add original list else add templist
                        if len(tempList)==0:
                            newdm_info[key]=value
                        else:
                            newdm_info[key]=tempList 
                    # else add value to dictionary
                    else:
                        newdm_info[key]=value
                logger.debug(f"writing raw domain info to {outfile}")
                json.dump(newdm_info,outfile)
        else:
            print(dm_info)
        return dm_info
    return {}

def formatDomainInfo(info:dict,domainFilestore:tuple):
    tp = 0
    logger.debug(f"creating file for writing [Files/{domainFilestore[0]}/formatDomainInfo.txt]")
    
    # if fileStoreBool is True: create file
    if domainFilestore[1]:
        outfile=open(f"Files/{domainFilestore[0]}/formatDomainInfo.txt","w+")
    for key,value in info.items():
        # if value is none: print or store to file
        if value == None:
            tp = 0
            logger.debug(f"writing formatted domain info to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}: {"None".rjust(32+4-len(key)-2," ")}\n")
            else:
                print(f"{key}: {"None".rjust(32+4-len(key)-2," ")}")
        
        # if value is type datetime: format value and write to file or print
        elif type(value) == datetime.datetime:
            tp = 1
            time = value.strftime('%m/%d/%Y at %H:%M:%S')
            logger.debug(f"writing formatted domain info to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}: {time.rjust(32+len(time)-len(key)-2," ")}\n")
            else:
                print(f"{key}: {time.rjust(32+len(time)-len(key)-2," ")}")
        
        # if value is type list loop through list looking for seperate types
        elif type(value) == list:
            #  write or print seperators
            if tp == 1 or tp == 0 or tp == 3:
                logger.debug(f"writing seperators to {outfile}")
                if domainFilestore[1]:
                    outfile.write("\n")
                else:
                    print("")
            tp = 2
            # write or print seperators
            logger.debug(f"writing seperators to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"{key}:\n")
            else:
                print(f"{key}:\n")

            for subValue in value:
                # if subvalue type is datime time format time else keep subValue
                if type(subValue) == datetime.datetime:
                    time = subValue.strftime('%m/%d/%Y at %H:%M:%S')
                    logger.debug(f"writing formatted domain info to {outfile}")
                    
                    #if fileStore is True: write to file else print
                    if domainFilestore[1]:
                        outfile.write(f"{time.rjust(32+len(time)," ")}\n")
                    else:
                        print(f"{time.rjust(32+len(time)," ")}")
                else:
                    logger.debug(f"writing formatted domain info to {outfile}") 
                    #if fileStore is True: write to file else print
                    if domainFilestore[1]:
                        outfile.write(f"{subValue.rjust(32+len(subValue)," ")}\n")
                    else:
                        print(f"{subValue.rjust(32+len(subValue)," ")}")
            
            #if fileStore is True: write to seperators to file
            logger.debug(f"writing seperators to {outfile}")
            if domainFilestore[1]:
                outfile.write(f"\n")
            else:
                print("")
        # value is not of the types mentioned above
        else:
            tp = 3
            logger.debug(f"writing formatted domain info to {outfile}")
            
            #if fileStore is True: write to file else print
            if domainFilestore[1]:
                outfile.write(f"{key}: {value.rjust(32+len(value)-len(key)-2," ")}\n")
            else:
                print(f"{key}: {value.rjust(32+len(value)-len(key)-2," ")}")
    outfile.close()