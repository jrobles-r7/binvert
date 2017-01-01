# binvert
Use Bing ip: searches to find the hostname of the provided ip addresses. Results should be verified...

 >usage: binvert.py [-h] [-i IPS] [-f FILENAME] [-p PAGES]
 >
 >Return the hostname of the supplied IP addresses using Bing
 >
 >optional arguments:
 >
 >-h, --help            show this help message and exit
 >
 >-i IPS, --ips IPS     Comma separated list of ip addresses
 >
 >-f FILENAME, --filename FILENAME
 >
 >File with one IP address per line
 >
 >-p PAGES, --pages PAGES
 >
 >Number of Bing pages to parse
 
# TODO
Organize the output. Group similar URIs(?), remove unique paths and only keep hosts(?)

Run host command on identified hostnames to verify results... I have seen a few inconsistencies... 
