#!/usr/bin/python2
import requests
import argparse
import subprocess
from lxml import html
from urlparse import urlparse
import sys
import re

def get_args():
    parser = argparse.ArgumentParser(description='Return the hostname of the supplied IP addresses using Bing')
    parser.add_argument('-i', '--ips',
        help='Comma separated list of ip addresses')
    parser.add_argument('-f', '--filename',
        help='File with one IP address per line')
    parser.add_argument('-p', '--pages', type=int, default=1,
        help='Number of Bing result pages to search through')
    return parser

def search(url,results):
    r = requests.get(url)
    tree =  html.fromstring(r.content)
    for node in tree.xpath("//div[@class='b_attribution']/cite"):
        results.append(node.xpath("normalize-space()"))
    return tree

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

    pages = 1 if args.pages < 1 else args.pages

    for ip_address in ip_addresses:
        urls = []
        base = 'https://www.bing.com/search?q=ip%3a'+ip_address
        tree = search(base,urls)

        counter = 2
        while counter <= pages:
            next_page = tree.xpath("//a[@aria-label='Page {0}']/@href".format(counter))
            if not next_page:
                break
            result_index = re.findall('&first=[0-9][0-9]*',next_page[0])[0].split('=')[1]
            tree = search(base+'&first='+result_index,urls)
            counter += 1

        print ip_address
        valid_net = []
        urls = list(set(urls))
        for url in urls:
            scheme = re.findall('^http(s|)://', url)
            if not scheme:
                url = 'http://' + url.split()[0]
            url = urlparse(url)
            ps = subprocess.Popen(('host', url.netloc), stdout=subprocess.PIPE)
            out = subprocess.check_output(('awk',"/has address/ {print $4}"), stdin=ps.stdout)
            ps.wait()
            if ip_address == out.strip():
                valid_net.append(url.netloc)
        print '\n'.join(list(set(valid_net)))
        print ''
