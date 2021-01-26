# -*- coding: UTF-8 -*-

from yaml import load, FullLoader
from pathlib import Path

from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'join_motd_reforged',
    'version': '1.0.0',
    'name': 'JoinMOTDR',
    'description': '',
    'author': [
        'Van_Involution',  # Reforged to fit MCDR 1.x
        'Alex3236'  # Source of inspiration
    ],
    'link': 'https://github.com/Van-Involution/MCDR-Plugins',
    'dependencies': {
        'mcdreforged': '>=1.0.0'
    }
}

NAME = PLUGIN_METADATA['name']
VERSION = PLUGIN_METADATA['version']
DEFAULT_CONFIG_PATH = f'config/{NAME}.yml'
DEFAULT_CONFIG = '''# Configure file for DayCountR

# 
# 
daycount: false

# 
# 

'''


def get_config(server: ServerInterface):
    if not Path(DEFAULT_CONFIG_PATH).is_file():
        server.logger.info('Fail to read config file, using default value')
        with open(file=DEFAULT_CONFIG_PATH, mode='w') as cfg_0:
            cfg_0.write(DEFAULT_CONFIG)
    with open(file=DEFAULT_CONFIG_PATH, mode='r') as cfg:
        return load(stream=cfg, Loader=FullLoader)


def get_day_count(server: ServerInterface):
    day_count_r = server.get_plugin_instance('day_count_reforged')
    return day_count_r.format_reply_msg(server)


def format_reply_msg(server: ServerInterface):
    config = get_config(server)
    reply_msg_list = [
        '-' * 10 + f'JoinMOTDR v{VERSION}' + '-' * 10, '\n'
    ]
    if config['daycount']:
        reply_msg_list.append(get_day_count(server) + '\n')
    reply_msg_list.append('-' * len(reply_msg_list[0]) + '\n')
    return RTextList(*reply_msg_list)


def on_player_joined(server: ServerInterface, player: str, info: Info):
    server.tell(player, format_reply_msg(server))
