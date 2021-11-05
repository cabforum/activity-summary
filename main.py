import subprocess
from typing import Any, Mapping, List
import argparse
import json
import sys
import os
import pathlib
import logging

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


def _config_to_json(configuration: List[config_types.MailingList]) -> str:
    return json.dumps(
        {
            m.address: _mailing_list_to_dict(m)
            for m in configuration
        }
    )


def _validate(configuration: List[config_types.MailingList]) -> bool:
    for mailing_list in configuration:
        if not mailing_list.validate():
            return False
        for repo in mailing_list.repositories:
            if not repo.validate():
                return False

    return True


def _send(configuration: List[config_types.MailingList]) -> None:
    pathlib.Path(MLS_JSON_DIR).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(MLS_JSON_DIR, mailing_lists_config.MLS_JSON_FILENAME), 'w') as f:
        f.write(_config_to_json(configuration))

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

if args.action == 'validate':
    result = _validate(mailing_lists_config.MAILING_LISTS_CONFIGURATION)
    if result:
        exit(0)
    else:
        exit(1)
elif args.action == 'send':
    _send(mailing_lists_config.MAILING_LISTS_CONFIGURATION)
else:
    raise ValueError(f'Unknown action "{args.action}"')
