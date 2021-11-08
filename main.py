import subprocess
from typing import Any, Mapping, List
import argparse
import json
import sys
import os
import pathlib
import logging
import re

import validators

import config_types
import mailing_lists_config


GITHUB_NOTIFY_ML_DIR = os.path.join(os.path.dirname(__file__), 'github-notify-ml')
MLS_JSON_DIR = os.path.join(GITHUB_NOTIFY_ML_DIR, 'instance')

MLS_SCRIPT_FILENAME = 'index.py'
ACTIVITY_BOT_CONFIG_FILENAME = 'config.json'


def _mailing_list_to_dict(mailing_list: config_types.MailingList) -> Mapping[str, Any]:
    return {
        f'digest:{mailing_lists_config.EXECUTION_DAY_LOWERCASE}': {
            'repos': [str(r) for r in mailing_list.repositories],
            'topic': mailing_list.name
        }
    }


def _get_destination_address(mailing_list: config_types.MailingList, test_address: str=None) -> str:
    if test_address is None:
        return mailing_list.address
    else:
        local_part, domain_part = test_address.split('@', maxsplit=1)

        list_name_alphanum = re.sub(r'\W', '', mailing_list.name)

        return f'{local_part}+{list_name_alphanum}@{domain_part}'


def _config_to_json(configuration: List[config_types.MailingList], test_address: str=None) -> str:
    return json.dumps(
        {
            _get_destination_address(m, test_address): _mailing_list_to_dict(m)
            for m in configuration
        }
    )


def _send(configuration: List[config_types.MailingList], test_address: str=None) -> None:
    pathlib.Path(MLS_JSON_DIR).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(MLS_JSON_DIR, mailing_lists_config.MLS_JSON_FILENAME), 'w') as f:
        f.write(_config_to_json(configuration, test_address))

    with open(os.path.join(MLS_JSON_DIR, ACTIVITY_BOT_CONFIG_FILENAME), 'w') as f:
        f.write(json.dumps(mailing_lists_config.ACTIVITY_BOT_CONFIGURATION))

    subprocess.check_call([
            sys.executable,
            MLS_SCRIPT_FILENAME,
            mailing_lists_config.EXECUTION_DAY_LOWERCASE.title()
        ],
        cwd=GITHUB_NOTIFY_ML_DIR
    )


logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['send', 'validate'])

args = parser.parse_args()

test_address = os.environ.get('TEST_ADDRESS')

if test_address:
    if not validators.email(test_address):
        raise ValueError(f'E-mail address "{test_address}" is not valid')
else:
    test_address = None

if args.action == 'validate':
    exit(
        0 if config_types.validate_configuration(mailing_lists_config.MAILING_LISTS_CONFIGURATION) else 1
    )
elif args.action == 'send':
    _send(mailing_lists_config.MAILING_LISTS_CONFIGURATION, test_address)
else:
    raise ValueError(f'Unknown action "{args.action}"')
