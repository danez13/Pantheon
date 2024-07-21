import whois
import datetime
import validators


def getDomainInfo(host:str) -> dict|None:
    if validators.domain(host):
        try:
            dm_info = whois.whois(host)
        except whois.parser.PywhoisError as error:
            raise error
        if type(dm_info) is None:
            raise AttributeError
        return dm_info

def formatDomainInfo(info:dict):
    ptp = 0
    tp = 0
    for key,value in info.items():
        if value == None:
            tp = 0
            print(f"{key}: {"None".rjust(32+4-len(key)-2," ")}")
        elif type(value) == datetime.datetime:
            tp = 1
            time = value.strftime('%m/%d/%Y at %H:%M:%S')
            print(f"{key}: {time.rjust(32+len(time)-len(key)-2," ")}")
        elif type(value) == list:
            if tp == 1 or tp == 0 or tp == 3:
                print("")
            tp = 2
            print(f"{key}:")
            for subValue in value:
                 if type(subValue) == datetime.datetime:
                    time = subValue.strftime('%m/%d/%Y at %H:%M:%S')
                    print(f"{time.rjust(32+len(time)," ")}")
                 else:
                    print(f"{subValue.rjust(32+len(subValue)," ")}")
        else:
            tp = 3
            print(f"{key}: {value.rjust(32+len(value)-len(key)-2," ")}")
        if tp == 2:
            print("")
