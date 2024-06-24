import os

from config_types import GithubRepository, MailingList


FROM_ADDRESS = 'infra-bot@cabforum.org'
FROM_NAME = 'Infrastructure Bot'
MLS_JSON_FILENAME = 'mls.json'
EXECUTION_DAY_LOWERCASE = 'sunday'

# USERS section
_USER_OFFICIAL = 'cabforum'

# MAILING LISTS section
_MAILING_LIST_CODE_SIGNING = MailingList(
    'Code Signing Certificate Working Group',
    'cscwg-public@cabforum.org',
    [
        GithubRepository(_USER_OFFICIAL, 'code-signing'),
    ]
)

_MAILING_LIST_SMIME = MailingList(
    'S/MIME Certificate Working Group',
    'smcwg-public@groups.cabforum.org',
    [
        GithubRepository(_USER_OFFICIAL, 'smime'),
    ]
)

_MAILING_LIST_SERVERCERT = MailingList(
    'Server Certificate Working Group',
    'servercert-wg@cabforum.org',
    [
        GithubRepository(_USER_OFFICIAL, 'servercert'),
    ]
)


_MAILING_LIST_NETSEC = MailingList(
    'Network Security Working Group',
    'netsec@cabforum.org',
    [
        GithubRepository(_USER_OFFICIAL, 'netsec'),
    ]
)


_MAILING_LIST_INFRASTRUCTURE = MailingList(
    'Infrastructure Subcommittee',
    'infrastructure@groups.cabforum.org',
    [
        GithubRepository(_USER_OFFICIAL, 'build-guidelines-action'),
        GithubRepository(_USER_OFFICIAL, 'activity-summary'),
    ]
)

_MAILING_LIST_FORUM = MailingList(
    'CA/B Forum',
    'public@groups.cabforum.org',
    [
        GithubRepository(_USER_OFFICIAL, 'forum'),
    ]
)

# TOP-LEVEL section
MAILING_LISTS_CONFIGURATION = [
    _MAILING_LIST_CODE_SIGNING,
    _MAILING_LIST_SMIME,
    _MAILING_LIST_SERVERCERT,
    _MAILING_LIST_NETSEC,
    _MAILING_LIST_INFRASTRUCTURE,
    _MAILING_LIST_FORUM,
]

ACTIVITY_BOT_CONFIGURATION = {
    'EMAIL_FROM': FROM_ADDRESS,
    'DIGEST_SENDER': FROM_NAME,
    'TEMPLATES_DIR': 'templates',
    'mls': os.path.join('instance', MLS_JSON_FILENAME)
}
