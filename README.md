## Student enrollment and background information

We currently have three information systems that the course staff has
to keep reconciled:

 - Official enrollment (FacultyCenter)
 - Course management system records
 - Cluster accounts

None of these systems talk to each other automatically.

In addition, there are two systems where account management can
basically be handled by students:

 - GitHub accounts
 - Piazza accounts

Beyond the basic data, there is also a HW0 assignment that gathers
information about the mapping between GitHub account IDs and netids,
background self-assessment, and a few free-form questions.

The scripts in this directory generate:

 - Plaintext netid lists from FacultyCenter and CMS
 - Differences between the FacultyCenter and CMS versions
 - A YAML file with netid/GitHub mappings and self-assessment info
 - Histograms of background self-assessment scores for students
