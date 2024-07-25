# Pantheon
information gathering and scanning Tool
## Modules
### InformationGathering
gather information about a target that can be used against it.

currently to do two actions:
- scraping
- domain lookup
#### scraping
scrape website for any details or information that can be found within. 

scraping has various sub-actions:
- link scraping: scrape website for links
- email scraping: scrape website for emails
- siteMapping: scrape a website and map the site

scraping carries various options:
-  page limit of scraped page
    - default = 1
- store details found to a file
- detailed scraping
    - scrape entire site for details

#### domain lookup
website domain information lookup

domain lookup one sub-action:
- format domain information

domain lookup one option:
- store information found to a file

### Scanning
scan targets for any piece of information that can be used to find vulnerabilties

currently to do one action:
- port scanning
#### Port scanning
scan ports checking if open or closed

port scanning has various options:
- limit: set a limit to how many ports to scan
    - default 65,535
- file store: store details found to a file
- open ports only: show only ports that are open on the target system


## Planned features:
- improve and add features to information gathering module
    - improve and add features to scrape action
    - improve and add features to domain look up action
- improve and add features to scanning module
    - improve and add features to port scanning module
- add exploitation module
- add maintaining access module
- add covering tracks module