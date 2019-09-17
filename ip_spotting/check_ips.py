'''
Parse (domain,ip) tuples from an input file (in tab-delimited format) and print
out any IPs that are inside one of the CIDRs defined in cidrs.tsv.

To test:

    (venv) $ python check_ips.py < test_ips.tsv
'''

import netaddr
import sys


cidrs = list()
cidr_dict = dict()

with open('cidrs.tsv') as i:
    for line in i:
        provider, block, name = map(str.strip, line.split('\t'))
        cidr = netaddr.IPNetwork(block)
        cidrs.append(cidr)
        cidr_dict[cidr] = {'provider': provider, 'name': name}


# This search is very slow because it checks all blocks. We could use
# netaddr.cidr_merge() to create a shorter list to check, but so far runtime has
# been acceptable.
for line in sys.stdin:
    domain, ip = map(str.strip, line.split('\t'))
    ip = netaddr.IPAddress(ip)
    for cidr in cidrs:
        if ip in cidr:
            d = cidr_dict[cidr]
            print('{} -> {} FOUND {} {} {}'.format(domain, ip, cidr,
                d['provider'], d['name']))
            break
