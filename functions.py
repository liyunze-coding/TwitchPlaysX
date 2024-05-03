import time
import subprocess
import platform
import socket
import re
import asyncio
import win32api  # Windows only
import win32con  # Windows only


class TwitchPlaysX:
    def __init__(self, key_delay, keymap, channel_name, x_limit) -> None:
        self.os = self.get_os()
        self.key_delay = key_delay
        self.keymap = keymap
        self.channel_name = channel_name.lower()
        self.x_limit = x_limit

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
                count = int(count or "1")
                if count > self.x_limit:
                    count = self.x_limit
                compiled_chars.extend([control] * count)
        return compiled_chars

    def process_message(self, author, message):
        characters = message.lower().split(" ")

        os_type = self.get_os()

        if self.all_valid_chars(characters):
            compiled_characters = self.compile_chars(characters)
            for char in compiled_characters:
                print(f"{author}: {char}")
                self.sendKey(char, os_type)

    async def listen(self):
        reader, writer = await asyncio.open_connection("irc.chat.twitch.tv", 6667)

        writer.write(f"NICK justinfan1234\r\n".encode("utf-8"))
        writer.write(f"JOIN #{self.channel_name}\r\n".encode("utf-8"))

        while True:
            data = await reader.read(2048)
            message = data.decode().strip()

            if message.startswith("PING"):
                writer.write(b"PONG\r\n")
                await writer.drain()

            elif message:
                author = message.split("!", 1)[0].split(":", 1)[-1]
                msg = (
                    message.split(f"#{self.channel_name.lower()}", 1)[-1]
                    .split(":", 1)[-1]
                    .strip()
                )
                self.process_message(author, msg)
