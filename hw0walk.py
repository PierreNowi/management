#!/usr/bin/env python

"""
Walks over the HW0 submissions (in the Submissions folder)
and generates a YAML file from it.
"""

import os
import re
import math
import yaml


# Ordinary text attributes
attr = {
    'name': '- First name',
    'netid': '- Cornell netid',
    'github': '- GitHub',
    'status': '- Status',
    'level': '- Level',
    'major': '- Major'}


# Self-assessment attributes
score_attr = {
    'git': '- Git:',
    'shell': '- Unix shell',
    'c': '- C programming',
    'python': '- Python programming',
    'architecture': '- Computer architecture',
    'concurrency': '- Locking and concurrency',
    'numerics': '- Numerical methods'}


def process_hw0(path):
    """Process a HW0 submission file

    Args:
        path (string): path to hw0.txt

    Returns:
        dictionary of attributes according to attr/score_attr
    """
    rec = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            for k, v in attr.items():
                if line.find(v) == 0:
                    field = re.search(":\s*(.*)$", line).group(1)
                    rec[k] = field
            for k, v in score_attr.items():
                if line.find(v) == 0:
                    field = re.search(":\s*(.*)$", line).group(1)
                    try:
                        rec[k] = math.floor(float(field))
                    except ValueError:
                        print("Could not convert {0}: {1}={2}".format(path, k, field))
    return rec


def walk_submissions(path):
    """Process all HW0 files under CMS submissions folder

    Args:
        path (string): path to submissions directory

    Returns:
        list of hw0 records
    """
    recs = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == 'hw0.txt':
                try:
                    recs.append(process_hw0("{0}/{1}".format(root, file)))
                except:
                    print('Issue with {0}'.format(root))
    return recs


if __name__ == "__main__":
    recs = walk_submissions("Submissions")
    with open('hw0.yml', 'w') as f:
        f.write(yaml.dump(recs, default_flow_style=False))
