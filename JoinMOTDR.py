# -*- coding: UTF-8 -*-

from re import match

from mcdreforged.api.decorator import new_thread
from mcdreforged.api.command import Literal
from mcdreforged.api.types import ServerInterface, Info, PlayerCommandSource
from mcdreforged.api.rtext import RText, RTextTranslation, RTextList, RAction

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
LINK = PLUGIN_METADATA['link']
VERSION = PLUGIN_METADATA['version']
DEFAULT_CONFIG_PATH = f'config/{NAME}.yml'
DEFAULT_PREFIX = '!!MOTDR'

config = dict()
error = 0b0


def get_config(server: ServerInterface):
    try:
        from yaml import load, FullLoader
    except Exception:
        server.logger.warning('Failed to import package PyYAML (https://pypi.org/project/PyYAML), use command "pip install PyYAML" to install!')
        return None
    else:
        try:
            with open(DEFAULT_CONFIG_PATH, 'r') as cfg:
                return load(cfg, FullLoader)
        except Exception:
            server.logger.warning(f'Config file disappeared, please download from {LINK}!')
            return None


def get_daycount(server: ServerInterface, plugin_id: str = 'day_count_reforged'):
    try:
        return RTextList(server.get_plugin_instance(plugin_id).get_day_count(server), '\n')
    except Exception:
        url = 'https://github.com/Van-Involution/DayCountR'
        warning = RText(f'§cFailed to get instance from plugin "§l{plugin_id}§r"').c(
            RAction.open_url, url).h(f'§lDocs§r: §n{url}§r')
        server.logger.warning(warning.to_plain_text())
        return RTextList(warning, '\n')


def get_seed(server: ServerInterface, plugin_id: str = 'seed_reforged'):
    try:
        return RTextList(server.get_plugin_instance(plugin_id).get_seed(server), '\n')
    except Exception:
        url = 'https://github.com/Van-Involution/SeedR'
        warning = RText(f'§cFailed to get instance from plugin "§l{plugin_id}§r"').c(
            RAction.open_url, url).h(f'§lDocs§r: §n{url}§r')
        server.logger.warning(warning.to_plain_text())
        return RTextList(warning, '\n')


def get_request_text(server: ServerInterface):
    global config
    from json import loads
    try:
        import requests
    except Exception:
        server.logger.warning('Failed to import package Requests (https://pypi.org/project/requests), use command "pip install requests" to install!')
        return None
    text = RTextList()
    for key_name, val_cfg in config.get('request_api_list', dict()).items():
        url = val_cfg.get('url', key_name)
        rtext_name = RTextList('[', RText(key_name).h(f'§lAPI§r: §n{url}§r').c(RAction.open_url, url), '] ')
        try:
            req_str = requests.get(url).text.strip()
            path = val_cfg.get('path', None)
            if path is not None:
                req_json: dict = loads(req_str)
                for item in path.split('/'):
                    req_json = req_json.get(item, dict())
                req_str = str(req_json).strip()
            text.append(rtext_name, RText(req_str).h(
                RTextList(rtext_name.to_plain_text(), RTextTranslation('chat.copy.click'))
            ).c(RAction.copy_to_clipboard, req_str), '\n')
        except Exception:
            warning = RText(f'§cFailed to get text from §n{url}§r')
            server.logger.warning(warning.to_plain_text())
            text.append(rtext_name, warning, '\n')
    return text


def get_bullshit(server: ServerInterface, plugin_id: str = 'bullshit_generator_api'):
    global config
    try:
        return server.get_plugin_instance(plugin_id).generate(
            keys=config.get('bullshit_keys', '§ktest§r'), breakline_chance=0
        )
    except Exception:
        url = 'https://github.com/Van-Involution/BullshitGenAPI'
        warning = RText(f'§cFailed to get instance from plugin "§l{plugin_id}§r"').c(
            RAction.open_url, url).h(f'§lDocs§r: §n{url}§r')
        server.logger.warning(warning.to_plain_text())
        return RTextList(warning, '\n')


def get_server_list(server: ServerInterface):
    global config
    sub_servers = config.get('server_list', dict())
    try:
        sub_server_list = RTextList()
        for key_id, val_server in sub_servers.items():
            name = RText(val_server.get('name', key_id)).h(RText(
                val_server.get('motd', f'/server {key_id}')
                .format(server_name=val_server.get('name', key_id))
            ))
            if not val_server.get('current', False):
                name.c(RAction.run_command, f'/server {key_id}')
            sub_server_list.append('[', name, ']')
        return sub_server_list.append('\n')
    except Exception:
        warning = RText(f'§cFailed to get config from plugin "§l{ID}§r"').c(
            RAction.open_url, LINK).h(f'§lDocs§r: §n{LINK}§r')
        server.logger.warning(warning.to_plain_text())
        return RTextList(warning, '\n')


def get_help(server: ServerInterface):
    global config
    try:
        return RText(
            config.get('help_message', '§7>>> Click for help message <<<§r')
        ).c(RAction.run_command, '!!help').h('§n!!help§r')
    except Exception:
        warning = RText(f'§cFailed to get config from plugin "§l{ID}§r"').c(
            RAction.open_url, LINK).h(f'§lDocs§r: §n{LINK}§r')
        server.logger.warning(warning.to_plain_text())
        return RTextList(warning, '\n')


def format_output(server: ServerInterface, player: str):
    global config, error
    error = 0b0
    func_list = {
        'daycount': get_daycount,
        'seed': get_seed,
        'spec_1': '\n',
        'request_text': get_request_text,
        'bullshit': get_bullshit,
        'spec_2': '\n',
        'server_list': get_server_list,
        'help': get_help
    }
    output = RTextList(
        RText(f'{"=" * 12} {config.get("title", f"{NAME} v{VERSION}")} {"=" * 12}\n')
        .h(f'§l{NAME} v{VERSION}§r').c(RAction.open_url, LINK),
        f'{config.get("welcome_message", "Welcome, §6{player_name}§r!").format(player_name=player)}\n'
    )
    for key, val in func_list.items():
        if key.startswith('spec_'):
            output.append(val)
        elif config.get(f'show_{key}', False):
            return_text = val(server)
            output.append(return_text)
    if bool(error):
        output.append(f'§cSomething of plugin {NAME} is going wrong, please let admins look up the console!§r')
    return output


def player_is_real(server: ServerInterface, player: str, bots: dict):
    def xstr(s): return str() if s is None else str(s)
    prefix, suffix = xstr(bots.get('prefix', None)), xstr(bots.get('suffix', None))
    if bool(prefix) or bool(suffix):
        bot_pattern = r'^' + prefix + r'.+' + suffix + r'$'
        return not bool(match(bot_pattern, player))
    else:
        server.logger.info(f'Cannot determine whatever player {player} is bot, still sent MOTD!')
        return True


@new_thread('Join MOTD Sender')
def on_player_joined(server: ServerInterface, player: str, info: Info):
    global config
    config = get_config(server)
    if config is not None:
        if player_is_real(server, player, config.get('bots', dict())):
            server.tell(player, format_output(server, player))
            server.logger.info(f'Succeeded to send MOTD to {player}')
        else:
            server.logger.info(f'Sent nothing because player {player} is bot')
    else:
        server.tell(player, f'§cFailed to get config of plugin {NAME}, please let admins look up the console!§r')


def on_load(server: ServerInterface, prev):
    def reply_message(src: PlayerCommandSource):
        try:
            on_player_joined(server, src.player, Info())
        except Exception:
            server.logger.info(f'Cannot send MOTD because command source is not player!')
    server.register_help_message(DEFAULT_PREFIX, 'Show MOTD of player join')
    server.register_command(
        Literal(DEFAULT_PREFIX).runs(reply_message)
    )
