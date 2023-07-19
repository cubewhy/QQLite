import builtins
import re

import requests
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


class Client(object):
    client_api = "http://127.0.0.1:5700"

    def __init__(self):
        object.__init__(self)

        self.events = []
        self.style_message = Style.from_dict({
            "uid": "#00ffff underline",
            "username": "#ffff00",
            "prompt": "#00ff00",
            "message": "#ffffff"
        })
        self.current_group = "0"

    def handle(self, event: dict):
        # print(event)
        self.events.append(event)  # add event to event list
        # Handle event
        match event["post_type"]:
            case 'message':
                gid: str | None = None
                uid: str = str(event["user_id"])
                if event["message_type"] == "group":
                    gid = str(event["group_id"])
                    if gid != self.current_group:
                        return
                    username: str = self.get_username(uid)
                else:
                    username: str = self.get_group_username(gid, uid)
                # print(event)
                message: str = event["raw_message"]
                fmt_msg = FormattedText([
                    ("class:username", username),
                    ("", " "),
                    ("class:uid", f"({uid})"),
                    ("class:prompt", " >>> "),
                    ("class:message", message)
                ])
                print(fmt_msg, style=self.style_message)
            case 'message_sent':
                gid: str | None = None
                uid = event["self_id"]
                if event["message_type"] == "group":
                    gid = str(event["group_id"])
                    if gid != self.current_group:
                        return
                    username = self.get_group_username(gid, uid)
                else:
                    username = self.get_self_username()
                message = event["message"]
                fmt_msg = FormattedText([
                    ("class:username", username),
                    ("", " "),
                    ("class:uid", f"({uid})"),
                    ("class:prompt", " <<< "),
                    ("class:message", message)
                ])
                print(fmt_msg, style=self.style_message)

    @classmethod
    def get_username(cls, uid: str | int):
        """QQ Username"""
        return requests.post(f"{cls.client_api}/get_stranger_info", data={
            "user_id": int(uid),
        }).json()["data"]["nickname"]

    @classmethod
    def get_self_username(cls):
        return str(requests.get(f"{cls.client_api}/get_login_info").json()["data"]["nickname"])

    @classmethod
    def send_message(cls, message_type: str, target: str | int, message: str):
        if message_type == "group":
            # Group message
            res = requests.post(f"{cls.client_api}/send_group_msg", data={
                "group_id": int(target),
                "message": message
            }).json()
        elif message_type == "private":
            # Private message
            res = requests.post(f"{cls.client_api}/send_private_msg", data={
                "user_id": int(target),
                "message": message
            }).json()
        else:
            res = {}  # Type not match
        try:
            return res["data"]["message_id"]
        except TypeError:
            return "Group not found"

    @classmethod
    def get_group_username(cls, gid: str | int, uid: str | int):
        return requests.post(f"{cls.client_api}/get_group_member_info", data={
            "group_id": int(gid),
            "user_id": int(uid),
            "no_cache": True
        }).json()["nickname"]

    @classmethod
    def get_group_name(cls, gid: str | int):
        try:
            return requests.post(f"{cls.client_api}/get_group_info", data={
                "group_id": int(gid),
                "no_cache": True
            }).json()["data"]["group_name"]
        except TypeError:
            return "GroupNotFound"

    @classmethod
    def find_cq(cls, message: str):
        """查找CQ Code"""
        codes = []
        p = re.findall(r"\[CQ:.*?]", message)
        builtins.print(p)
        if p is None:
            return []
        for code in p:
            codes.append(cls.parse_cq(code))
        return codes

    @classmethod
    def parse_cq(cls, code: str):
        cq = {"data": {}}
        type_with_args = code[1:-1].split(",")
        for i, value in enumerate(type_with_args):
            if i == 0:
                cq["type"] = value[3:]
            else:
                d = value.split("=")
                cq['data'][d[0]] = d[1]
        return cq


instance = Client()
