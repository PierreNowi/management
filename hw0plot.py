#!/usr/bin/env python

"""
Plot histograms of the HW0 self-assessment results.
"""

import yaml
import numpy as np
import matplotlib.pyplot as plt


def gather_scores(recs, name):
    """Gather a set of 1-5 scores from student response records

    Args:
        recs: list of student responses
        name: name of self-assessment score to consider

    Returns:
        length-5 histogram of how many self-assessed as levels 1-5
    """
    scores = np.zeros(5)
    for rec in recs:
        if name in rec:
            scores[int(rec[name]-1)] += 1
    return scores


def score_plot(recs, name):
    """Produce a histogram plot file for a HW0 score.

    Args:
        recs: list of student responses
        name: name of self-assessment score to consider
    """
    ind = np.arange(5)+1
    scores = gather_scores(recs, name)
    plt.figure()
    plt.bar(ind-0.4, scores, 0.8)
    plt.title(name)
    plt.savefig("hw0-{0}.pdf".format(name))


if __name__ == "__main__":
    attrs = ['git', 'shell', 'c', 'python', 'architecture',
             'concurrency', 'numerics']
    with open("hw0.yml", "r") as f:
        recs = yaml.load(f)
    for attr in attrs:
        score_plot(recs, attr)

