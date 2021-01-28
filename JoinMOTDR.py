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
        'Alex3236',  # Source of inspiration
        'Fallen_Breath'  # Another source of inspiration
    ],
    'link': 'https://github.com/Van-Involution/JoinMOTDR',
    'dependencies': {
        'mcdreforged': '>=1.0.0'
    }
}

ID = PLUGIN_METADATA['id']
NAME = PLUGIN_METADATA['name']
VERSION = PLUGIN_METADATA['version']
DEFAULT_CONFIG_PATH = f'config/{NAME}.yml'
DEFAULT_CONFIG = '''# Configure file for JoinMOTDR
# Check https://github.com/Van-Involution/JoinMOTDR for detail

# Basic settings
welcome_message: Welcome, §6{player_name}§r!  # Use {player_name} as format key, support RText
show_help: true
help_message: "§7>>> Click for help message <<<§r"  # Support RText

# MCDR plugin requires
show_daycount: false  # Requires plugin DayCountR (https://github.com/Van-Involution/DayCountR)
show_seed: false  # Requires plugin SeedR (https://github.com/Van-Involution/SeedR)
show_bullshit: false  # Requires plugin BullshitGenAPI (https://github.com/Van-Involution/BullshitGenAPI)
bullshit_keys:  # Support RText
- §ktest§r

# Other API requires
bots:  # For fake player detection
  prefix: #bot_
  suffix: #_fake
show_request_text: false  # Requires package Requests (https://pypi.org/project/requests/), use command "pip install requests" to install
request_api_list:  # Make sure the return is plain text
  §bHitokoto§r: https://v1.hitokoto.cn/?encode=text
show_server_list: false  # For sub-server of server-group
server_list:  # Use format as the first object
  survival:  # Server ID, be used in command "/server <server_id>"
    name: Survival  # Displayed server name
    motd: You are now in server §a§l{server_name}§r  # Use {server_name} as format key, support RText
    current: true  # Optional, for server in the same directory
  creative:
    name: Creative
    motd: Click to join server §b{server_name}§r
  mirror:
    name: Mirror
    motd: Click to join server §b{server_name}§r
'''


def get_config(server: ServerInterface):
    if not Path(DEFAULT_CONFIG_PATH).is_file():
        server.logger.info('Fail to read config file, using default value')
        with open(file=DEFAULT_CONFIG_PATH, mode='w') as cfg_0:
            cfg_0.write(DEFAULT_CONFIG)
    with open(file=DEFAULT_CONFIG_PATH, mode='r') as cfg:
        return load(stream=cfg, Loader=FullLoader)


def get_day_count(server: ServerInterface, plugin_id: str = 'day_count_reforged'):
    try:
        return server.get_plugin_instance(plugin_id).get_day_count(server)
    except Exception:
        server.logger.warning(f'Failed to get data of plugin "{plugin_id}"')
        return None


def get_seed(server: ServerInterface, plugin_id: str = 'seed_reforged'):
    try:
        return server.get_plugin_instance(plugin_id).get_seed(server)
    except Exception:
        server.logger.warning(f'Failed to get data of plugin "{plugin_id}"')
        return None


def get_request_text(server: ServerInterface, config: dict):
    try:
        import requests
    except Exception:
        server.logger.warning('Failed to import package Requests, if it\'s not installed, use command "pip install requests" to install')
        return None
    text = RTextList()
    for item, url in config.get('request_api_list', dict()).items():
        try:
            text.append(
                '[', RText(item).h(f'§lAPI§r: §n{url}§r').c(RAction.open_url, url), '] ',
                requests.get(url).text, '\n'
            )
        except Exception:
            server.logger.warning(f'Failed to get text from {url}')
    return text


def get_bullshit(server: ServerInterface, config: dict, plugin_id: str = 'bullshit_generator_api'):
    try:
        return server.get_plugin_instance(plugin_id).generate(config.get('bullshit_keys', '§ktest§r'))
    except Exception:
        server.logger.warning(f'Failed to get data of plugin "{plugin_id}"')
        return None


def get_help_msg(server: ServerInterface, help_msg: str):
    try:
        return RText(help_msg).c(RAction.run_command, '!!help').h('!!help')
    except Exception:
        server.logger.warning(f'Failed to get config of plugin "{ID}"')
        return None


def get_server_list(server: ServerInterface, sub_servers: dict):
    try:
        sub_server_list = RTextList()
        for key_id, val_server in sub_servers.items():
            if val_server.get('current', False):
                sub_server_list.append(
                    '[',
                    RText(name := val_server.get('name', key_id), RColor.red, RStyle.bold)
                    .h(RText(
                        val_server.get('motd', 'You are now in server §a§l{server_name}§r')
                        .format(server_name=name)
                    )),
                    '] '
                )
            else:
                sub_server_list.append(
                    '[',
                    RText(name := val_server.get('name', key_id), RColor.gold)
                    .h(RText(
                        val_server.get('motd', 'Click to join server §b{server_name}§r')
                        .format(server_name=name)
                    ))
                    .c(RAction.run_command, f'/server {key_id}'),
                    '] '
                )
        return sub_server_list
    except Exception:
        server.logger.warning(f'Failed to get config of plugin "{ID}"')
        return None


def format_output(server: ServerInterface, player: str, cfg: dict):
    error = 0b0
    output = RTextList(
        f'{"-" * 8}JoinMOTDR v{VERSION}{"-" * 8}\n\n',
        cfg.get('welcome_message', 'Welcome, §6{player_name}§r!').format(player_name=player),
        '\n'
    )
    if cfg.get('show_daycount', False):
        if (day_count := get_day_count(server)) is not None:
            output.append(day_count, '\n')
        else:
            server.logger.warning('Failed to add "daycount" to MOTD')
            error |= 0b1
    if cfg.get('show_seed', False):
        if (seed := get_seed(server)) is not None:
            output.append(seed, '\n')
        else:
            server.logger.warning('Failed to add "seed" to MOTD')
            error |= 0b1
    output.append('\n')
    if cfg.get('show_request_text', False):
        if (request_text := get_request_text(server, cfg)) is not None:
            output.append(request_text)
        else:
            server.logger.warning('Failed to add "request_text" to MOTD')
            error |= 0b1
    if cfg.get('show_bullshit', False):
        if (bullshit := get_bullshit(server, cfg)) is not None:
            output.append(bullshit, '\n')
        else:
            server.logger.warning('Failed to add "bullshit" to MOTD')
            error |= 0b1
    output.append('\n')
    if cfg.get('show_server_list', False):
        if (server_list := get_server_list(server, cfg.get('server_list', None))) is not None:
            output.append(server_list, '\n')
        else:
            server.logger.warning('Failed to add "server_list" to MOTD')
            error |= 0b1
    if cfg.get('show_help', True):
        if (help_msg := get_help_msg(server, cfg.get('help_message', None))) is not None:
            output.append(help_msg, '\n')
        else:
            server.logger.warning('Failed to add "help_message" to MOTD')
            error |= 0b1
    if bool(error):
        output.append(f'§cSomething of {NAME} is going wrong, please let admins look up the console!§r')
    return output


def player_is_real(server: ServerInterface, player: str, bots: dict):
    def xstr(s): return '' if s is None else str(s)
    prefix, suffix = xstr(bots.get('prefix', None)), xstr(bots.get('suffix', None))
    if bool(prefix) or bool(suffix):
        bot_pattern = r'^' + prefix + r'.+' + suffix + r'$'
        return not bool(re.match(bot_pattern, player))
    else:
        server.logger.info(f'Cannot determine whatever player {player} is bot, still sent MOTD!')
        return True


def on_player_joined(server: ServerInterface, player: str, info: Info):
    config = get_config(server)
    if player_is_real(server, player, config.get('bots', dict())):
        server.tell(player, format_output(server, player, config))
        server.logger.info(f'Succeeded to send MOTD to {player}')
    else:
        server.logger.info(f'Sent nothing because player {player} is bot')
