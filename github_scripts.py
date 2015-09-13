from github import Github, UnknownObjectException
import getpass
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

def get_repo_pull_requests(repo_name, user_name=None,
                           organization_name="cornell-cs5220-f15"):
    """Get the pull requests associated with a given repository.

    Inputs:
    repo_name (str) - The name of the repository.
    user_name (str) - The name of the user that owns the repository.
    organization_name (str) - The name of the organization that owns the repository.
    """
    username = raw_input("Username: ")
    password = getpass.getpass()
    if username == '':
        g = Github()
    else:
        # You do not need to enter username/password here. However, Github rate-limits
        # requests made from IPs without logins, so you could get throttled if you don't.
        g = Github(username, password)
    if user_name is None:
        org = g.get_organization(organization_name)
        repo = org.get_repo(repo_name)
    elif organization_name is None:
        user = g.get_user(user_name)
        repo = user.get_repo(repo_name)
    else:
        raise ValueError("get_pull_request_users: Both user_name and organization_name are None")

    return repo.get_pulls()

def get_pull_request_users(repo_name, user_name=None, 
                           organization_name="cornell-cs5220-f15"):
    """Get the Github usernames of all users who have made pull requests to a repo.

    Note that either user_name or organization_name should be None, but not
    both.

    Inputs:
    repo_name (str) - The name of the repository.
    user_name (str) - The name of the user that owns the repository.
    organization_name (str) - The name of the organization that owns the repository.

    Outputs:
    pull_usernames (list) - The Github usernames of those who have made pull
                            requests to a repository.
    """
    pulls = get_repo_pull_requests(repo_name, user_name, organization_name)
    
    pull_usernames = []
    for pull in pulls:
        pull_usernames.append(pull.user.login)

    return pull_usernames

def get_pull_request_content(directory, filename, repo_name, user_name=None,
                             organization_name="cornell-cs5220-f15"):
    """Get the contents of a specific file in each pull request repository.

    For each pull request against a repo, go to a specific file within the head
    of the pull request and retrieve that file's contents.
    Note: This function retrieves actual file content. If you do not use an
    authenticated login when get_repo_pull_requests() prompts for it, you are
    likely to get rate limited by Github.

    Inputs:
    directory (str) - The directory of the file of interest.
    filename (str) - The name of the file of interest.
    repo_name (str) - The name of the repository.
    user_name (str) - The name of the user that owns the repository.
    organization_name (str) - The name of the organization that owns the repository.
    
    Output:
    username2contents (dict) - A dictionary whose keys are github usernames and
       whose values are file contents. If a pull request's repo doesn't contain
       the filename of interest, then the value is None.
    """
    pulls = get_repo_pull_requests(repo_name, user_name, organization_name)

    username2contents = {}
    for p in pulls:
        prepo = p.head.repo
        username = prepo.owner.login
        full_filename = directory + '/' + filename
        try:
            file_contents = prepo.get_contents(full_filename).decoded_content
            username2contents[username] = file_contents
        except UnknownObjectException:
            username2contents[username] = None
    
    return username2contents

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
