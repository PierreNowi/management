#!/usr/env python

"""
Scrapes the hw0.yml file for the list of netids not listed as dropped.
"""

import yaml

with open('hw0.yml', 'r') as f:
    recs = yaml.load(f)
    netids = [rec['netid'] for rec in recs if 'drop' not in rec]
    netids.sort()

with open('netids-hw0.txt', 'w') as f:
    for netid in netids:
        f.write("{0}\n".format(netid));
