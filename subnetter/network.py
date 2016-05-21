#!/usr/bin/env python3
import ipaddress
import json
import argparse
import math
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


class Subnet:
    network = None

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


def create_config_from_template(file, attr):
    env = Environment()
    env.loader = FileSystemLoader('../templates')
    config = env.get_template(file)

    return config.render(attr)


def get_network_attributes(subnet, port):
    attr = {
        'port': port,
        'row': subnet.name,
        'network': str(subnet.network.network_address),
        'gateway': str(subnet.network[1]),
        'start': str(subnet.network[2]),
        'start_next': str(subnet.network[3]),
        'end': str(subnet.network[-2]),
        'netmask': subnet.network.netmask,
    }
    return attr


def main():
    parser = argparse.ArgumentParser(description="Divide networks based on JSON description")
    parser.add_argument('-n', '--network', dest='network_file', default='network.json', action='store',
                        help='File containing network description in JSON format', required=False)

    args = parser.parse_args()

    with open(args.network_file) as json_file:
        json_data = json.load(json_file)

    for part in json_data:
        network = ipaddress.ip_network(part["network"])
        total = 0
        largest_network = 32
        smallest_network = 0
        network_list = []
        print("Dividing {}:".format(network))
        for subnet in part["subnets"]:
            if subnet["number"] == 0:
                continue
            if "per-row" not in subnet:
                subnet["per-row"] = 1

            total += int(math.pow(2, 32-subnet["size"]) * subnet["number"] * subnet["per-row"])
            
            if subnet["size"] < largest_network:
                    largest_network = subnet["size"]
            if subnet["size"] > smallest_network:
                    smallest_network = subnet["size"]
            
            if subnet["number"] > 1:
                for i in range(0, subnet["number"]):
                    if subnet["per-row"] > 1:
                        for j in range(0, subnet["per-row"]):
                            network_list.append(Subnet(subnet["size"], "{}-{}-{}".format(subnet["name"], i+1, j+1)))
                    else:
                        network_list.append(Subnet(subnet["size"], "{}-{}".format(subnet["name"], i+1)))
            else:
                network_list.append(Subnet(subnet["size"], subnet["name"]))
        
        if total > network.num_addresses:
            print("Can't fit subnets into network :(")
            return 1
        
        done = False
        network = list(network.subnets(new_prefix=largest_network))
        while not done:
            if len(network) == 0:
                print("Can't fit subnets into network :(")
                return 1
        
            for net in network_list:
                if net.size == largest_network and net.network is None:
                    net.network = network.pop(0)

            largest_network += 1
            if largest_network > smallest_network:
                break
            network = split_network(list(network))
            done = True
            for net in network_list:
                if net.network is None:
                    done = False
                    break

        attributes = {
            "subnets": []
        }
        for i in range(len(network_list)):
            attributes["subnets"].append(get_network_attributes(network_list[i], i+1))

        print(create_config_from_template(part["template"], attributes))

        # print(network)

    return 0

if __name__ == "__main__":
    main()
