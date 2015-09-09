#!/usr/bin/env python

"""
List auditors in the class
"""

import yaml

if __name__ == "__main__":
    with open("hw0.yml", "r") as f:
        recs = yaml.load(f)
        for rec in recs:
            if 'drop' not in rec and rec['status'] == 'audit':
                print(rec['netid'])

