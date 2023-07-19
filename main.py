import sys
from threading import Thread

from prompt_toolkit.shortcuts import input_dialog

import client
from client import Client
from server import start_server
from terminal import get_input


def main():
    the_server = Thread()
    the_server.run = start_server
    the_server.start()

    qq_username = Client.get_self_username()

    try:
        while True:
            user_input = get_input(qq_username)
            # pase_command
            match user_input:
                case ".exit":
                    sys.exit()
                case ".group":
                    gid = input_dialog(
                        title='Group Switcher',
                        text='Enter group ID:').run()
                    client.instance.current_group = gid
                    continue
            client.instance.send_message("group", client.instance.current_group, user_input)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
