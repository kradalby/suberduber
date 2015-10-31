#!/usr/bin/env python3
import ipaddress
import json
import argparse
import math


class Subnet:
    network = None
    assigned = False

    def __init__(self, size, name):
        self.size = size
        self.name = name
        
    def __str__(self):
        return "{}: {}".format(self.name, self.network)

    def __unicode__(self):
        return self.name
        
    def __repr__(self):
        return str(self)
     

def split_network(network):
    new_network = []
    for net in network:
        new_network.extend(list(net.subnets()))
        
    return new_network


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test xDC Analogue")
    parser.add_argument('-n', '--network', dest='network_file', default='network.json', action='store', help='File containing network description in JSON format', required=False)
    
    args = parser.parse_args()
    
    with open(args.network_file) as json_file:
        json_data = json.load(json_file)
    
    network = ipaddress.ip_network(json_data["network"])
    total = 0
    largest_network = 32
    network_list = []
    
    for subnet in json_data["subnets"]:
        if subnet["number"] == 0:
            continue
        
        total += int(math.pow(2, 32-subnet["size"]) * subnet["number"])   
        
        if subnet["size"] < largest_network:
                largest_network = subnet["size"]
        
        if subnet["number"] > 1:
            for i in range(1, subnet["number"]+1):
                network_list.append(Subnet(subnet["size"], "{} {}".format(subnet["name"], i)))
        else:
            network_list.append(Subnet(subnet["size"], subnet["name"]))
    
    if total > network.num_addresses:
        print("Can't fit subnets into network :(")
        exit(1)
    
    done = False
    network = list(network.subnets(new_prefix=largest_network))
    while not done:
        if len(network) == 0:
            print("Can't fit subnets into network :(")
            exit(1)
    
        for net in network_list:
            if net.size == largest_network and not net.assigned:
                net.network = network.pop(0)
                net.assigned = True
        
        done = True
        network = split_network(list(network))
        largest_network += 1
        for net in network_list:
            if net.assigned == False:
                done = False
               
    for net in network_list:
        print(net)
    