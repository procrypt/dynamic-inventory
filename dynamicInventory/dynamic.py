#!/usr/bin/env python

import argparse
import json
import csv
import yaml


class Inventory(object):

    def __init__(self):
        self.inventory = {"_meta": {"hostvars": {}}}
        self.parse_cli_args()

        if self.args.list:
            self.inventory = self.final_inventory()
            self.inventory = self.inventory
        else:
            self.inventory = self.inventory

        print json.dumps(self.inventory)

    def open_yml_file(self, ymlFile):
        fileData = open(ymlFile)
        vars = yaml.load(fileData)
        return vars

    def open_csv_file(self, csvFile):
        fileData = open(csvFile)
        header = next(fileData)
        csv_file = csv.reader(fileData, delimiter="\t")
        data = []
        for line in enumerate(csv_file):
            data.append(line)
        fileData.close()
        return data, header

    def read_dynamic_inventory(self):
        inventory = self.inventory
        (csvData, header) = self.open_csv_file('data.csv')
        return csvData,header

    def hostdata(self):
        (csvData, header) = self.read_dynamic_inventory()

        # Same as host vars but not in a list
        hostdata = []
        for a in csvData:
            for b in a[1]:
                hostdata.append(b)

        return hostdata

    def host(self):
        inventory = self.inventory
        hostdata = self.hostdata()

        # Iterate over list of hostvars
        hostvars = []
        for i in hostdata:
            for j in i.split(","):
                hostvars.append(j)

            inventory["_meta"]["hostvars"].update({hostvars[1]: {}})
            hostvars = []

        return inventory

    def group(self):
        (csvData, header) = self.read_dynamic_inventory()
        hostdata = self.hostdata()

        # Iterate over list of hostvars
        group = {}
        hostvars = []
        for i in hostdata:
            for j in i.split(","):
                hostvars.append(j)

            # data = dict(zip(headerData, hostvars))
            if hostvars[0] in group.keys():
                group[hostvars[0]]["hosts"].append(hostvars[1])
            else:
                group.update({hostvars[0]: {"hosts": [hostvars[1]]}})
                a = hostvars[0]
                yml = self.open_yml_file("group_vars/"+a)
                group.update({hostvars[0]: {"hosts": [hostvars[1]], "vars": yml}})
            hostvars = []
        return group


    def final_inventory(self):

        group_vars = self.group()
        host_vars = self.host()

        inventory = group_vars.copy()
        inventory.update(host_vars)

        return inventory

    def parse_cli_args(self):
        parser = argparse.ArgumentParser(description='Produce an Ansible Inventory from a file')
        parser.add_argument('--list', action='store_true', help='List Hosts')
        parser.add_argument('--host', action='store', help='Get all the variables about a specific host')

        self.args = parser.parse_args()


Inventory().final_inventory()
