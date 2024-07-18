import json
import urllib.parse

def populateSiteMap(siteMap:dict,parts:urllib.parse.SplitResult):
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
    with open(f"Files/{parts.hostname}/Map.json","w+") as outfile:
        json.dump(siteMap,outfile)
    return siteMap