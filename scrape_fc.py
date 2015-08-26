#!/usr/env python

"""
Scrapes the Excel file produced by faculty center to get
the current list of netids.
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(open("ps.xls"))

netids = []
for row in soup.find_all('tr'):
    tds = row.find_all('td')
    if len(tds) > 3:
        netids.append(tds[3].string)
netids.sort()

with open('netids-fc.txt', 'w') as f:
    for netid in netids:
        f.write("{0}\n".format(netid));
