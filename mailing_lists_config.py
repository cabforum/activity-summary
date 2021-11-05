import os

import config_types


FROM_ADDRESS = 'infra-bot@cabforum.org'
FROM_NAME = 'Infrastructure Bot'
MLS_JSON_FILENAME = 'mls.json'
EXECUTION_DAY_LOWERCASE = 'sunday'

# USERS section
_USER_OFFICIAL = 'cabforum'

# MAILING LISTS section
_MAILING_LIST_CODE_SIGNING = config_types.MailingList(
    'Code Signing Certificate Working Group',
    'cscwg-public@cabforum.org',
    [
        config_types.GithubRepository(_USER_OFFICIAL, 'code-signing'),
    ]
)

_MAILING_LIST_SMIME = config_types.MailingList(
    'S/MIME Certificate Working Group',
    'smcwg-public@cabforum.org',
    [
        config_types.GithubRepository(_USER_OFFICIAL, 'smime'),
    ]
)

# TOP-LEVEL section
MAILING_LISTS_CONFIGURATION = [
    _MAILING_LIST_CODE_SIGNING,
    _MAILING_LIST_SMIME,
]

ACTIVITY_BOT_CONFIGURATION = {
    'EMAIL_FROM': FROM_ADDRESS,
    'DIGEST_SENDER': FROM_NAME,
    'TEMPLATES_DIR': 'templates',
    'mls': os.path.join('instance', MLS_JSON_FILENAME)
}
