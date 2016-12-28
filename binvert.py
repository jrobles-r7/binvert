#!/usr/bin/python2
import requests
import argparse
from lxml import html
import sys

def get_args():
    parser = argparse.ArgumentParser(description='Return the hostname of the supplied IP addresses using Bing')
    parser.add_argument('-i', '--ips',
        help='Comma separated list of ip addresses')
    parser.add_argument('-f', '--filename',
        help='File with one IP address per line')

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

    for ip_address in ip_addresses:
        r = requests.get("https://www.bing.com/search?q=ip%3a"+ip_address)
        tree =  html.fromstring(r.content)
        print ip_address
        for node in tree.xpath("//div[@class='b_attribution']/cite"):
            print node.xpath("normalize-space()")
        print ''