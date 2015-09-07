#!/usr/bin/env python

"""
Find who dropped
"""

import yaml


if __name__ == "__main__":
    with open("hw0.yml", "r") as f:
        recs = yaml.load(f)
    with open("netids-fc.yml", "r") as f:
        netids = yaml.load(f)
        netid_lookup = {}
        for netid in netids:
            netid_lookup[netid] = netid
    for rec in recs:
        if 'netid' in rec:
            netid = rec['netid']
            if netid not in netid_lookup:
                print(rec['netid'])
        else:
            print(rec)
