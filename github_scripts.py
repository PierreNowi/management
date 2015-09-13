from github import Github
import yaml
import smtplib
import sys

###
# Scripts for interacting with Github programmatically.
#
# This relies on the PyGithub module, with can be installed with
# easy_install PyGithub
# or
# pip install PyGithub
#
# Source: http://jacquev6.net/PyGithub/v1/introduction.html
###

def github_netid_mapping(hw0_filename):
    """Generate mapping dictionaries between github usernames and Cornell netIDs."""
    with open(hw0_filename, 'r') as f:
        recs = yaml.load(f)
    github2netid = {}
    netid2github = {}
    for rec in recs:
        github = rec["github"]
        netid = rec["netid"]
        github2netid[github] = netid
        netid2github[netid]  = github
    return github2netid, netid2github

def read_netid_list(filename):
    """Read in a list of netIDs.

    Inputs:
    filename (str) - The name of the file containing the netIDs.
    """
    netids = []
    with open(filename, 'r') as f:
        for line in f:
            netids.append(line.rstrip())
    return netids

def get_pull_request_users(repo_name, user_name=None, 
                           organization_name="cornell-cs5220-f15"):
    """Get the Github usernames of all users who have made pull requests to a repo.

    Note that either user_name or organization_name should be None, but not
    both.

    Inputs:
    repo_name (str) - The name of the repository.
    user_name (str) - The name of the user that owns the repository.
    organization_name (str) - The name of the organization that owns the repository.

    """
    g = Github()
    if user_name is None:
        org = g.get_organization(organization_name)
        repo = org.get_repo(repo_name)
    elif organization_name is None:
        user = g.get_user(user_name)
        repo = user.get_repo(repo_name)
    else:
        raise ValueError("get_pull_request_users: Both user_name and organization_name are None")
    
    pull_usernames = []
    for pull in repo.get_pulls():
        pull_usernames.append(pull.user.login)

    return pull_usernames

def netids_without_pull_requests(repo_name, user_name=None,
                                 organization_name="cornell-cs5220-f15",
                                 hw0_filename="hw0.yml",
                                 netid_list_filename="student_netids.csv"):
    """Get the netIDs of all students who have not made pull requests to a repo.

    Note that either user_name or organization_name should be None, but not
    both.

    Inputs:
    repo_name (str) - The name of the repository.
    user_name (str) - The name of the user that owns the repository.
    organization_name (str) - The name of the organization that owns the 
                              repository.
    hw0_filename (str) - The filename containing hw0 yaml data.
    netid_list_filename (str) - The filename containing the list of all 
                                currently enrolled students, as exported from 
                                CMS.

    """
    pull_usernames = get_pull_request_users(repo_name, user_name,
                                            organization_name)
    github2netid, netid2github = github_netid_mapping(hw0_filename)

    pull_netids = []
    for pu in pull_usernames:
        pull_netids.append(github2netid[pu])

    class_netids = read_netid_list(netid_list_filename)

    netids_without_pull_requests = []
    for netid in class_netids:
        if netid not in pull_netids:
            netids_without_pull_requests.append(netid)

    return netids_without_pull_requests


if __name__ == "__main__":
    # Use: python github_scripts.py lecture
    print "Email addresses of students who have not yet made pull requests"
    print "; ".join([s + "@cornell.edu" for s in netids_without_pull_requests(sys.argv[1])])
