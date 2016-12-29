#!/usr/bin/python2
import requests
import argparse
from lxml import html
import sys
import re

#add a flag for number of pages to search through
def get_args():
    parser = argparse.ArgumentParser(description='Return the hostname of the supplied IP addresses using Bing')
    parser.add_argument('-i', '--ips',
        help='Comma separated list of ip addresses')
    parser.add_argument('-f', '--filename',
        help='File with one IP address per line')
    parser.add_argument('-p', '--pages', type=int, default=1,
        help='Number of Bing result pages to search through')

    return parser

if __name__ == '__main__':
    parser = get_args()
    args = parser.parse_args()

    ip_addresses = []
    if args.ips:
        ip_addresses += args.ips.split(',')
    if args.filename:
        with open(args.filename, 'r') as f:
            for line in f.readlines():
                ip_addresses.append(line.strip())

    if not ip_addresses:
        print "No IP addresses specified\n"
        print parser.print_help()
        sys.exit(1)

    #pages
    pages = 1 if args.pages < 1 else args.pages

    #view bing search results. figure out xpath for going to the next page
    for ip_address in ip_addresses:
        base = 'https://www.bing.com/search?q=ip%3a'+ip_address
        r = requests.get(base)
        tree =  html.fromstring(r.content)
        urls = []
        for node in tree.xpath("//div[@class='b_attribution']/cite"):
            urls.append(node.xpath("normalize-space()"))

        counter = 2
        while counter <= pages:
            next_page = tree.xpath("//a[@aria-label='Page {0}']/@href".format(counter))
            if not next_page:
                break
            result_index = re.findall('&first=[0-9][0-9]*',next_page[0])[0].split('=')[1]

            r = requests.get(base+'&first='+result_index)
            tree =  html.fromstring(r.content)
            for node in tree.xpath("//div[@class='b_attribution']/cite"):
                urls.append(node.xpath("normalize-space()"))
            counter += 1
        print ip_address
        print '\n'.join(list(set(urls)))
        print ''
