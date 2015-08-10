#!/usr/bin/env python3
'''
File: suberduber.py
Author: Kristoffer Dalby
Description: Tool for generating bulk of repetitive config files
'''

import argparse
import ipaddress

from math import ceil, log

from jinja2 import Template

# Dev
# from pprint import pprint


def get_subnet_address(mask_bits):
    bits = []
    string = ''
    c = 0
    while c < 32:
        if c < mask_bits:
            string += '1'
        else:
            string += '0'
        if len(string) == 8:
            bits.append(string)
            string = ''
        c += 1
    bits = list(map(lambda x: str(int(x, 2)), bits))
    return '.'.join(bits)


def get_network_attributes(ip_network, mask, row, port):
    attr = {
        'port': port,
        'row': row,
        'network': str(ip_network[0]),
        'gateway': str(ip_network[1]),
        'start': str(ip_network[2]),
        'end': str(ip_network[-2]),
        'netmask': get_subnet_address(mask),
    }
    return attr


def create_config_from_template(file, attr):
    with open(file, 'r') as c:
        config = Template(c.read())
        return config.render(attr)


def get_rows(rows, switch_per_row):
    r = []
    for row in range(1, rows + 1):
        for switch in range(1, switch_per_row + 1):
            r.append('row-{}-{}'.format(row, switch))
    return r

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='suberduber.py, creating them config files')

    parser.add_argument('-r', '--rows', action='store', dest='rows', type=int, required=True)
    parser.add_argument('-s', '--switch', action='store', dest='switch_per_row', type=int, required=True)
    parser.add_argument('-m', '--mask', action='store', dest='mask', type=int, required=True)
    parser.add_argument('-ns', '--network-start', action='store', dest='network_start', required=True)
    parser.add_argument('-f', '--file', action='store', dest='file', required=True)

    args = parser.parse_args()

    per = args.switch_per_row
    rows = args.rows
    file = args.file
    switch_mask_bit = args.mask
    network_start = args.network_start

    total_network_size = 32 - (ceil(log(per * rows * (2 ** (32 - switch_mask_bit)), 2)))
    networks = list(ipaddress.ip_network('{}/{}'.format(network_start, total_network_size)).subnets(new_prefix=switch_mask_bit))

    row_names = get_rows(rows, per)

    for i in range(len(row_names)):
        print(create_config_from_template(file, get_network_attributes(networks[i], switch_mask_bit, row_names[i], i + 1)))
