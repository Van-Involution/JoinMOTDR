# JoinMOTDR

[English](README.md) | **中文**

> **注意**：JoinMOTDR 基于 [**MCDR v1.x**](https://github.com/Fallen-Breath/MCDReforged) 开发，并且**不支持** MCDR v0.x

**JoinMOTDR** 是一个 MCDR 插件，由 [TISUnion](https://github.com/TISUnion)/[**joinMOTD**](https://github.com/TISUnion/joinMOTD) 重制而成，当玩家进入服务器时自动向其发送自定义消息，并提供 `!!MOTDR` 命令随时查看消息。

## 安装插件

### 最新发布

在 [**Releases 页面**](https://github.com/Van-Involution/JoinMOTDR/releases)下载最新的 `JoinMOTDR-<版本号>.zip`，解压后将 `JoinMOTDR.py` 放入 `plugins/` 目录中，并将 `JoinMOTDR.yml` 放入 `config/` 目录中。

### 最新源码

将仓库克隆（`git clone`）至 `plugins/` 目录中，复制一份 `JoinMOTDR.yml` 放入 `config/` 目录中，并按如下代码块编辑 **MCDR 实例**的 `config.yml`：

```YAML
# The list of directory path where MCDR will search for plugin to load
# Example: "path/to/my/plugin/directory"
plugin_directories:
- plugins
- plugins/JoinMOTDR
```

## 使用插件

### 配置

插件在生成 MOTD 时会读取路径为 `cinfig/JoinMOTDR.yml` 的配置文件，若找不到配置文件则会报错，并提醒下载具有如下内容的默认配置文件：

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

以下为各配置项的解释：

#### 基本设置

**基本设置**无需依赖任何外源 API（MCDR 插件或其他 API），是插件消息的基本组成部分；以下为各项本类设置的解释：

- `title`：MOTD 的标题，将会显示在整个消息的第一行，带有内容为 `JoinMOTDR - <版本号>` 的悬浮文本
- `welcome_message`：欢迎消息，紧随标题显示，生成文本时字符串中的 `{player_name}` 会被替换为玩家名称
- `show_help`：是否显示帮助消息
- `help_message`：帮助消息，将会显示在整个消息的最后一行，点击执行命令 `!!help`

#### 依赖 MCDR 插件的设置

**依赖 MCDR 插件的设置**需要依赖至少一个 MCDR 插件，当无法获取依赖插件的实例时，对应设置项将不起作用，并且聊天栏和控制台都会显示对应的报错消息；以下为各项本类设置的解释：

- `show_daycount`：是否显示开服天数，依赖 [**DayCountR**](https://github.com/Van-Involution/DayCountR)
- `show_seed`：是否显示服务器存档种子，依赖 [**SeedR**](https://github.com/Van-Involution/SeedR)
- `show_bullshit`：是否显示狗屁不通文章，依赖 [**BullshitGen**](https://github.com/Van-Involution/BullshitGen)
- `bullshit_keys`：生成狗屁不通文章的关键词**列表**，支持[**格式化代码**](https://minecraft-zh.gamepedia.com/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81)

#### 依赖其他 API 的设置

**依赖其他 API 的设置**需要依赖有效的外源API（即非 MCDR 相关的 API），当无法获取外源 API 的正确返回值时，对应设置项将不起作用，并且聊天栏和控制台都会显示对应的报错消息；以下为各项本类设置的解释：

- `bots`：假人识别相关，目前已在地毯端通过测试
  - `prefix`：假人前缀
  - `suffix`：假人后缀
- `show_request_text`：是否显示网络请求文本，需要 Python 模块 [**Requests**](https://pypi.org/project/requests)，可在控制台用 `pip install requests` 命令安装
- `request_api_list`：网络请求 API **列表**，设置详情见下：
  - `<title>`：请求文本的标题，显示在正文前
    - `url`：请求文本的链接，目前支持纯文本和 JSON 的返回值
    - `path`：请求文本在 JSON 对象中的路径，暂不支持列表中的元素；留空则按照纯文本解析
- `show_server_list`：是否显示服务器列表，目前已在 [**Bungeecord**](https://github.com/SpigotMC/BungeeCord) 和 [**Waterfall**](https://github.com/PaperMC/Waterfall) 等服务端通过测试
- `server_list`：服务器**列表**，设置详情见下：
  - `<server_id>`：服务器 ID，用于切换服务器的命令 `/server <server_id>` 中，可查看转发服务器的配置文件以获取
    - `name`：显示出的服务器名称，支持[**格式化代码**](https://minecraft-zh.gamepedia.com/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81)，留空则使用服务器 ID
    - `motd`：切换按钮的悬浮文本，支持[**格式化代码**](https://minecraft-zh.gamepedia.com/%E6%A0%BC%E5%BC%8F%E5%8C%96%E4%BB%A3%E7%A0%81)
    - `current`：*可选项*，是否处于该服务器中，留空默认为 `false` 且点击按钮可执行切服命令，若为 `true` 则点击无反应

### 命令

插件提供 `!!MOTDR` 命令随时查看插件发送的消息，当命令源并非真实玩家时将不会向命令源发送消息。
