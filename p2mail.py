from __future__ import print_function

import yaml
import gmail_helper as GMail


gmail = GMail.GMailSender()

with open("hw0.yml", "r") as f:
    recs = yaml.load(f)

with open("proj2.yml", "r") as f:
    teams = yaml.load(f)

student_names = {}
for rec in recs:
    if 'name' in rec:
        netid = rec['netid']
        name = rec['name']
        student_names[netid] = name

template = """
Dear all,

For the second assignment, I am suggesting different groups.
I would like to again recommend that groups contain a mix of
application folks and CS folks.  Below is your recommended team;
if my records are not up-to-date and people have dropped, or if
I have teamed you with someone you cannot work with, please use
Piazza to rearrange.

David

Team {0}
--------
{1}
"""

group_id = 0
for team in teams:
    group_id += 1
    member_ids = ""
    recipients = ["bindel@cs.cornell.edu",
                  "cponce@cs.cornell.edu", "ehl59@cornell.edu"]
    for m in team['members']:
        netid = m['netid']
        recipients.append("{0}@cornell.edu".format(netid))
        member_ids += '{0} ({1})\n'.format(student_names[netid], netid)
    tofield = ",".join(recipients)
    print(template.format(group_id, member_ids))
    gmail.send("david.bindel@gmail.com", tofield, "Project 2 groups",
               template.format(group_id, member_ids))
    
