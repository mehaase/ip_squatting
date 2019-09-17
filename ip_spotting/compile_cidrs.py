'''
Convert IP blocks (CIDRs) from proprietary formats provided by various vendors
into a consolidated CSV.

The output format is:

    <PROVIDER>[TAB]<PREFIX>[TAB]<BLOCK_NAME>

That is, the provider, CIDR prefix, and block name (if available) are saved in
tab-delimited format, one block per line.
'''

import dns.resolver, json, netaddr

blocks = list()

print('Loading amazon…')
with open('aws-cidrs.json') as f:
    aws_blocks = json.load(f)

for prefix in aws_blocks['prefixes']:
    if prefix['service'] == 'AMAZON':
        # "AMAZON" is a special keyword that means an IP block associated with
        # any service. The same blocks will show up under other services, too,
        # so we can ignore it here.
        continue
    name = f'{prefix["service"]}-{prefix["region"]}'
    blocks.append(('amazon', prefix['ip_prefix'], name))

print('Loading alibaba…')
with open('ali-baba-whois.txt') as f:
    fiter = iter(f)
    for line in fiter:
        if line.startswith('inetnum:'):
            start, end = map(str.strip, line[16:].split('-'))
            cidrs = netaddr.iprange_to_cidrs(start, end)
            line = next(fiter)
            if line.startswith('netname:'):
                name = line[16:].strip()
            else:
                name = ''
            for cidr in cidrs:
                blocks.append(('alibaba', str(cidr), name))

print('Loading azure…')
def process_azure_file(path):
    with open(path) as f:
        azure_public_blocks = json.load(f)
        for net in azure_public_blocks['values']:
            props = net['properties']
            name = net['name']
            for prefix in props['addressPrefixes']:
                blocks.append(('azure', prefix, name))
process_azure_file('azure-gov.json')
process_azure_file('azure-public.json')

print('Loading google… (via DNS)')
resolver = dns.resolver.Resolver()
to_check = list()
checked = set()
for result in resolver.query('_cloud-netblocks.googleusercontent.com', 'TXT'):
    txt = result.to_text().strip('"')
    assert txt.startswith('v=spf1')
    for part in txt.split():
        if part.startswith('include:'):
            to_check.append(part[8:])
for name in to_check:
    checked.add(name)
    for result in resolver.query(name, 'TXT'):
        txt = result.to_text().strip('"')
        assert txt.startswith('v=spf1')
        for part in txt.split():
            if part.startswith('include:'):
                new_name = part[8:]
                if new_name not in checked:
                    to_check.append(new_name)
            elif part.startswith('ip4:'):
                blocks.append(('google', part[4:], ''))

print('Writing cidrs.tsv… ({} blocks)'.format(len(blocks)))
with open('cidrs.tsv', 'w') as o:
    for block in blocks:
        o.write(f'{block[0]}\t{block[1]}\t{block[2]}\n')

print('Done')
