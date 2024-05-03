import time
import subprocess
import platform
import socket
import re
import asyncio
import win32api  # Windows only
import win32con  # Windows only


class TwitchPlaysX:
    def __init__(self, key_delay, keymap, channel_name, x_limit, kill_commands) -> None:
        self.os = self.get_os()
        self.key_delay = key_delay
        self.keymap = keymap
        self.channel_name = channel_name.lower()
        self.x_limit = x_limit
        self.kill_commands = kill_commands

    # not tested
    def sendKeyLinux(self, button):
        subprocess.run(["xdotool", "key", button])
        time.sleep(self.key_delay)

    def sendKeyWindows(self, button):
        win32api.keybd_event(self.keymap[button], 0, 0, 0)
        time.sleep(self.key_delay)
        win32api.keybd_event(self.keymap[button], 0, win32con.KEYEVENTF_KEYUP, 0)

    def get_os(self):
        os_name = platform.system()
        if os_name == "Windows":
            return "Windows"
        elif os_name == "Linux":
            return "Linux"
        else:
            return "Unknown"

    def sendKey(self, button, os_type):
        if os_type.lower() == "windows":
            self.sendKeyWindows(button)
        else:
            self.sendKeyLinux(button)

    def all_valid_chars(self, char_array):
        pattern = re.compile(r"^[a-z]+\d*$")
        return all(pattern.match(char) for char in char_array)

    def compile_chars(self, char_array):
        compiled_chars = []
        for char in char_array:
            match = re.match(r"([a-z]+)(\d*)", char)
            if match:
                control, count = match.groups()
                if control not in self.keymap:
                    return []
                count = int(count or "1")
                if count > self.x_limit:
                    count = self.x_limit
                compiled_chars.extend([control] * count)

        return compiled_chars

    def process_message(self, author, message, is_mod):
        if is_mod and (message.lower() in self.kill_commands):
            print("Killing TwitchPlaysX")
            exit()

        characters = message.lower().split(" ")

        os_type = self.get_os()

        compiled_characters = self.compile_chars(characters)
        for char in compiled_characters:
            print(f"{author}: {char}")
            self.sendKey(char, os_type)

    async def play(self):
        reader, writer = await asyncio.open_connection("irc.chat.twitch.tv", 6667)

        writer.write(f"NICK justinfan1234\r\n".encode("utf-8"))
        writer.write(
            f"CAP REQ :twitch.tv/tags\r\n".encode("utf-8")
        )  # Enable IRCv3 tags
        writer.write(f"JOIN #{self.channel_name}\r\n".encode("utf-8"))

        while True:
            data = await reader.read(2048)
            message = data.decode().strip()

            if message.startswith("PING"):
                writer.write(b"PONG\r\n")
                await writer.drain()

            elif message:
                tags, author, msg = message.split(" ", 2)
                author = author.split("!", 1)[0].split(":", 1)[-1]
                msg = (
                    msg.split(f"#{self.channel_name.lower()}", 1)[-1]
                    .split(":", 1)[-1]
                    .strip()
                )

                is_mod = ("user-type=mod" in tags) or (
                    "badges=broadcaster" in tags
                )  # Check if the user is a moderator

                self.process_message(author, msg, is_mod)
