#!/usr/bin/env python

"""
Plot histograms of the HW0 self-assessment results.
"""

import yaml


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
        if (name in rec) and ('drop' not in rec):
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
    for field in ['status', 'level', 'major']:
        print("===== {0} ======".format(field))
        print_counts(uniq_field(recs, field))
