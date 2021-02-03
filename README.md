# JoinMOTDR

**English** | [中文](README_cn.md)

> **Note**: JoinMOTDR is developed based on [**MCDR v1.x**](https://github.com/Fallen-Breath/MCDReforged), and **DO NOT** support MCDR v0.x

**JoinMOTDR** ioa a MCDR plugin, reforged from [TISUnion](https://github.com/TISUnion)/[**joinMOTD**](https://github.com/TISUnion/joinMOTD), send customized message while player joined server, and provide command `!!MOTDR` to get MOTD anywhere.

## Installation

### Latest Release

Download latest `JoinMOTDR-<version>.zip` from [**Releases Page**](https://github.com/Van-Involution/JoinMOTDR/releases) and unzip it, then put `JoinMOTDR.py` into `plugins/` directory and `JoinMOTDR.yml` into `config/` directory.

### Latest Source Code

Clone this repository (`git clone`) into `plugins/` directory and put a copy of `JoinMOTDR.yml` into `config/` directory, then edit `config.yml` of **MCDR instance** as the following codeblock:

```YAML
# The list of directory path where MCDR will search for plugin to load
# Example: "path/to/my/plugin/directory"
plugin_directories:
- plugins
- plugins/JoinMOTDR
```

## Usages

### Config

Plugin will read config file in `cinfig/JoinMOTDR.yml`, if failed to read it will raise an exception, then remind to download default config file with content as the following:

```YAML
# Configure file for JoinMOTDR
# Check https://github.com/Van-Involution/JoinMOTDR for detail

# Basic Settings
title: JoinMOTDR # Title of the whole MOTD
welcome_message: Welcome, §6§l{player_name}§r!  # Use {player_name} as format key, support formatting codes
show_help: true # At the end of the whole MOTD
help_message: "§7>>> Click for help message <<<§r"  # Support formatting codes

# MCDR Plugin Requires
show_daycount: false  # Requires plugin DayCountR (https://github.com/Van-Involution/DayCountR)
show_seed: false  # Requires plugin SeedR (https://github.com/Van-Involution/SeedR)
show_bullshit: false  # Requires plugin BullshitGen (https://github.com/Van-Involution/BullshitGen)
bullshit_keys:  # Support formatting codes
- §ktest§r

# Other API Requires
bots:  # For fake player detection
  prefix: #bot_
  suffix: #_fake
show_request_text: false  # Requires package Requests (https://pypi.org/project/requests/), use command "pip install requests" to install
request_api_list:  # Make sure the return is plain text or JSON
  §d§lPoetry§r:  # Displayed name of the request text
    url: https://api.muxiaoguo.cn/api/Gushici  # URL of the request API
    path: data/Poetry  # Path from root object of JSON return, leave a blank for plain text
  §6§liCiBa§r:
    url: http://open.iciba.com/dsapi
    path: content
  §b§lHitokoto§r:
    url: https://v1.hitokoto.cn/?encode=text
    path:
show_server_list: false  # For sub server of server group
server_list:  # Use format as the first object
  survival:  # Server ID, be used in command "/server <server_id>"
    name: §c§l§nSurvival§r  # Displayed server name
    motd: You are now in server {server_name}  # Use {server_name} as format key, support formatting codes
    current: true  # Optional, for server in the same directory
  creative:
    name: §6Creative§r
    motd: Click to join server {server_name}
  mirror:
    name: §6Mirror§r
    motd: Click to join server {server_name}
```

The following are explanations of all settings:

#### Basic Settings

**Basic Settings** DO NOT require any outside API (MCDR plugins or other API), it is the basic part of plugin message; the following are explanations of all settings in this type:

- `title`: Title of MOTD, will be displayed on the first line of the whole message, with hover text `JoinMOTDR - <version>`
- `welcome_message`: Welcome message of MOTD, follows the title, `{player_name}` in the string will be replaced by name of player when generate text
- `show_help`: Whatever display help message
- `help_message`: Help message, will be displayed on the last line of the whole message, click to run command `!!help`

#### MCDR Plugin Requires

**MCDR Plugin Requires** AT LEAST require one MCDR plugin, if failed to get instance of required plugin, setting will NOT work, exception message will display on console and chat bar; the following are explanations of all settings in this type:

- `show_daycount`: Whatever display day count of server set up, requires [**DayCountR**](https://github.com/Van-Involution/DayCountR)
- `show_seed`: Whatever display server level seed, requires [**SeedR**](https://github.com/Van-Involution/SeedR)
- `show_bullshit`: Whatever display bullshit article, requires [**BullshitGen**](https://github.com/Van-Involution/BullshitGen)
- `bullshit_keys`: **List** of key words to generate bullshit article, support [**Formatting codes**](https://minecraft.gamepedia.com/Formatting_codes)

#### Other API Requires

**Other API Requires** DO require outside API, if failed to get correct return value of API, setting will NOT work, exception message will display on console and chat bar; the following are explanations of all settings in this type:

- `bots`: About fake players detection, passed test on carpet server for now
  - `prefix`: Prefix of fake players
  - `suffix`: Suffix of fake players
- `show_request_text`: Whatever display request text, DO requires Python moudle [**Requests**](https://pypi.org/project/requests), can use command `pip install requests` in console to install
- `request_api_list`: **List** of request API, detail follows: 
  - `<title>`: Title of request text, displays before content
    - `url`: Link of request text, support return value of plain text and JSON for now
    - `path`: Path of request text in JSON object, DO NOT support meMber in list for now; leave a blank to parse as plain text
- `show_server_list`: Whatever display list of server, passed test on [**Bungeecord**](https://github.com/SpigotMC/BungeeCord) and [**Waterfall**](https://github.com/PaperMC/Waterfall) for now
- `server_list`: **List** of server, detail follows:
  - `<server_id>`: ID of server, be used in server-switch command `/server <server_id>`, can get from config file of proxy server
    - `name`:  Displayed name of server, supports [**Formatting codes**](https://minecraft.gamepedia.com/Formatting_codes), leave a blank to use ID of server
    - `motd`: Hover text of switch botton, supports [**Formatting codes**](https://minecraft.gamepedia.com/Formatting_codes)
    - `current`: *Optional*, whatever be in this server, leave a blank to use default value `false` and click botton to run switch command, if use `true` then nothing will happen when click

### Command

Plugin provided a command `!!MOTDR` to get MOTD anywhere, but it will reply nothing if command source is NOT real player.
