# Pantheon
Information Gathering and Scanning Tool
## Modules
### InformationGathering
Gather information about a target that can be used against it.

Currently can do two actions:
- scraping
- domain lookup
  
#### Scraping
Scrape website for any details or information that can be found within. 

Scraping has various sub-actions:
- link scraping: scrape website for links
- email scraping: scrape website for emails
- siteMapping: scrape a website and map the site

Scraping carries various options:
-  page limit of scraped page
    - default = 1
- store details found to a file
- detailed scraping
    - scrape entire site for details

#### Domain Lookup
Website domain information lookup

Domain lookup has one sub-action:
- format domain information

Domain lookup has one option:
- store information found to a file

### Scanning
Scan targets for any piece of information that can be used to find vulnerabilities.

Currently can do one action:
- port scanning

#### Port Scanning
Scan ports checking if open or closed

Port scanning has various options:
- limit: set a limit to how many ports to scan
    - default 65,535
- file store: store details found to a file
- open ports only: show only ports that are open on the target system

## Planned Features:
- improve and add features to information gathering module
    - improve and add features to scrape action
    - improve and add features to domain look up action
- improve and add features to scanning module
    - improve and add features to port scanning module
- add exploitation module
- add maintaining access module
- add covering tracks module
