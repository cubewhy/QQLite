import os

from prompt_toolkit import prompt, HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

import client

user_dir = os.path.expanduser("~")
config_dir = os.path.join(user_dir, ".cubewhy", "qqLite")
history = os.path.join(config_dir, "historyChat.txt")


def init():
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(history):
        open(history, "w").close()


CommandCompleter = WordCompleter([
    ".exit",
    ".download",
    ".msg"
])


def bottom_toolbar():
    return HTML(f'QQ Lite | TargetGroup: {client.instance.get_group_name(client.instance.current_group)} ({client.instance.current_group})')


def get_input(username: str):
    style = Style.from_dict({
        'username': "ansicyan",
        "prompt": "#00aa00"
    })

    message = [
        ("class:username", username),
        ("class:prompt", " >>> ")
    ]
    user_input = prompt(message, style=style, history=FileHistory(history), auto_suggest=AutoSuggestFromHistory(),
                        completer=CommandCompleter, vi_mode=True, multiline=True, mouse_support=True,
                        bottom_toolbar=bottom_toolbar
                        )
    return user_input
