#!/usr/bin/env python

"""
Plot histograms of the HW0 self-assessment results.
"""

import yaml


level = {'MS' : 'Master',
         'MEng' : 'Master',
         'MPS' : 'Master',
         'PhD' : 'PhD',
         'ugrad' : 'ugrad',
         'prof': 'prof'}

area = {'CS' : 'CS/IS',
        'IS' : 'CS/IS',
        'ECE': 'ECE',
        'MAE': 'App',
        'CEE': 'App',
        'MSE': 'App',
        'ChemE': 'App',
        'ORIE': 'App',
        'AEP': 'App',
        'Chemistry': 'App',
        'Physics': 'App',
        'EAS': 'App',
        'Statistics': 'App',
        'CAM': 'App',
        'Math': 'App',
        'Independent': 'App'}


def major(majors):
    if isinstance(majors, list):
        return list(map(major, majors))
    elif majors in area:
        return area[majors]
    else:
        return majors


def edit_recs(recs):
    for rec in recs:
        rec['level'] = level[rec['level']]
        rec['major'] = major(rec['major'])
        rec['tag'] = "{0} {1}".format(rec['major'], rec['level'])

def uniq_field(recs, name):
    """Find number of unique instances of a value in records.

    Args:
        recs: List of records
        name: Name of common field

    Returns:
        map from keys to number of occurrences
    """
    s = {}
    for rec in recs:
        if (name in rec) and ('drop' not in rec) and (rec['status'] == 'enrolled'):
            fields = rec[name]
            if not isinstance(fields, list):
                fields = [fields]
            for field in fields:
                if field in s:
                    s[field] += 1
                else:
                    s[field] = 1
    return s


def print_counts(s):
    for v,k in s.items():
        print("{0}: {1}".format(v,k))


if __name__ == "__main__":
    with open("hw0.yml", "r") as f:
        recs = yaml.load(f)
    edit_recs(recs)
    for field in ['level', 'major', 'tag']:
        print("===== {0} ======".format(field))
        print_counts(uniq_field(recs, field))
