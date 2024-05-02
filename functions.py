import time
import subprocess
import platform
import socket
import win32api  # Windows only
import win32con  # Windows only


class TwitchPlaysX:
    def __init__(self, key_delay, keymap, channel_name) -> None:
        self.os = self.get_os()
        self.key_delay = key_delay
        self.keymap = keymap
        self.channel_name = channel_name

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
        return all(char in self.keymap for char in char_array)

    def process_message(self, author, message):
        characters = message.lower().split(" ")

        os_type = self.get_os()

        if self.all_valid_chars(characters):
            for char in characters:
                print(f"{author}: {char}")
                self.sendKey(char, os_type)

    def twitch_chat_listener(self, channel):
        server = "irc.chat.twitch.tv"
        port = 6667
        nick = "justinfan123"  # Twitch allows anonymous users with 'justinfan' prefix
        channel = f"#{channel}"

        sock = socket.socket()
        sock.connect((server, port))
        sock.send(f"NICK {nick}\r\n".encode("utf-8"))
        sock.send(f"JOIN {channel}\r\n".encode("utf-8"))

        while True:
            resp = sock.recv(2048).decode("utf-8")

            if resp.startswith("PING"):
                sock.send("PONG\n".encode("utf-8"))

            # Check if message is not empty
            elif len(resp) > 0:
                # Extract author from response
                author = resp.split("!", 1)[0].split(":", 1)[-1]

                # Extract message from response
                msg = resp.split(channel, 1)[-1].split(":", 1)[-1].strip()

                self.process_message(author, msg)
