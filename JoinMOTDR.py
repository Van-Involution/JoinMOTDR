# -*- coding: UTF-8 -*-

import re
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

welcome_message: Welcome, §6{player_name}§r!
show_daycount: false
show_seed: false
show_help: true
help_message: "§7>>> Click for help message <<<§r"
show_servers: false
servers:
  survival:
    name: Survival
    motd: You are now in server §a§l{server_name}§r
    current: true
  creative:
    name: Creative
    motd: Click to join server §b{server_name}§r
  mirror:
    name: Mirror
    motd: Click to join server §b{server_name}§r
  qmirror:
    name: qMirror
    motd: Click to join server §b{server_name}§r
current_server: survival
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


def get_seed(server: ServerInterface):
    seed_r = server.get_plugin_instance('seed_reforged')
    return seed_r.get_seed(server)


def get_help_msg(help_msg: str = '>>>Click to get help message<<<'):
    return RText(help_msg).c(RAction.run_command, '!!help').h('!!help')


def get_sub_servers(sub_servers: dict):
    sub_server_list = []
    for item in sub_servers:
        if sub_servers[item].get('current', False):
            sub_server_list.append(RTextList(
                '[',
                RText(sub_servers[item]['name'], RColor.red, RStyle.bold)
                .h(RText(sub_servers[item]['motd'].format(server_name=sub_servers[item]['name']))),
                '] '
            ))
        else:
            sub_server_list.append(RTextList(
                '[',
                RText(sub_servers[item]['name'], RColor.gold)
                .h(RText(sub_servers[item]['motd'].format(server_name=sub_servers[item]['name'])))
                .c(RAction.run_command, f'/server {item}'),
                '] '
            ))
    return RTextList(*sub_server_list)


def format_reply_msg(server: ServerInterface, player: str):
    config = get_config(server)
    reply_msg_list = [
        f'{"-" * 8}JoinMOTDR v{VERSION}{"-" * 8}\n\n',
        RText(config["welcome_message"].format(player_name=player)), '\n'
    ]
    if config['show_daycount']:
        reply_msg_list.append(get_day_count(server))
        reply_msg_list.append('\n')
    if config['show_seed']:
        reply_msg_list.append(get_seed(server))
        reply_msg_list.append('\n')
    reply_msg_list.append('\n')
    if config['show_servers']:
        reply_msg_list.append(get_sub_servers(config['servers']))
        reply_msg_list.append('\n')
    if config['show_help']:
        reply_msg_list.append(get_help_msg(config["help_message"]))
        reply_msg_list.append('\n')
    return RTextList(*reply_msg_list)


def player_is_real(server: ServerInterface, player: str):
    with open('config.yml', 'r') as mcdr_cfg_yml:
        mcdr_cfg = load(mcdr_cfg_yml, FullLoader)
        server_dir: str = mcdr_cfg['working_directory']
    with open(file=f'{server_dir}\\server.properties', mode='r') as server_prop:
        for prop_line in server_prop.readlines():
            if (reeeee := re.match(r'^level-name=(.*)', prop_line)) is not None:
                level_dir: str = reeeee.group(1)
                break
    if Path(carpet_conf_path := f'{server_dir}\\{level_dir}\\carpet.conf').is_file():
        with open(file=carpet_conf_path, mode='r') as carpet_conf:
            for conf_line in carpet_conf.readlines():
                if (reeeee1 := re.match(r'^fakePlayerNamePrefix ([^#]*)', conf_line)) is not None:
                    prefix = reeeee1.group(1)
                elif (reeeee2 := re.match(r'^fakePlayerNameSuffix ([^#]*)', conf_line)) is not None:
                    suffix = reeeee2.group(1)
        if bool(prefix) or bool(suffix):
            bot_pattern = r'^' + prefix + r'.+' + suffix + r'$'
            return bool(re.match(bot_pattern, player))
        else:
            server.logger.info(f'Cannot determine whatever player {player} is bot')
            return True


def on_player_joined(server: ServerInterface, player: str, info: Info):
    if player_is_real(server, player):
        server.tell(player, format_reply_msg(server, player))
        server.logger.info(f'Succeeded to send MOTD to {player}')
    else:
        server.logger.info(f'Sent nothing because player {player} is bot')
