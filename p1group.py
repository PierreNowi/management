#!/usr/bin/env python

"""
Assign groups for project 1
"""

import yaml
import random


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


def group_merit(group_attributes, member):
    """Compute merit for adding a proposed member to a group.

    +10: New major (CS/IS, ECE, App)
    +1: New level (ugrad, PhD, Master)
    """
    merit = 0
    if member['level'] not in group_attributes:
        merit += 1
    if isinstance(member['major'], list):
        for major in member['major']:
            if major not in group_attributes:
                merit += 10
                break
    else:
        if member['major'] not in group_attributes:
            merit += 2
    return merit


def group_add(group, member):
    """Add a member to a group
    """
    member['in_group'] = True
    group['members'].append(member)
    group[member['level']] = True
    if isinstance(member['major'], list):
        for major in member['major']:
            group[major] = True
    else:
        group[member['major']] = True
    return group


def form_group(recs, nmembers):
    group = {'members': []}
    for k in range(nmembers):
        best = (None, -1)
        for rec in recs:
            if (rec['status'] == 'enrolled' and
                'drop' not in rec and 'in_group' not in rec):
                merit = group_merit(group, rec)
                if merit > best[1]:
                    best = (rec, merit)
        if best[1] < 0:
            break
        group_add(group, best[0])
    return group


def form_groups(recs):
    group = form_group(recs, 3)
    while len(group['members']) == 3:
        print("==============")
        for m in group['members']:
            print("{0} ({1})".format(m['netid'], m['tag']))
        group = form_group(recs, 3)

        
if __name__ == "__main__":
    with open("hw0.yml", "r") as f:
        recs = yaml.load(f)
    edit_recs(recs)
    for field in ['level', 'major', 'tag']:
        print("===== {0} ======".format(field))
        print_counts(uniq_field(recs, field))
    random.shuffle(recs)
    form_groups(recs)
