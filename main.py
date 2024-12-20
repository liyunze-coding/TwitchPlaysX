import win32con  # Windows only
from functions import TwitchPlaysX
import platform
import asyncio

# SETTINGS
CHANNEL_NAME = "CHANNEL_NAME"  # Twitch channel name
KEY_DURATION = 500  # (milliseconds) duration of each key press
KEY_DELAY = 0.1
X_LIMIT = 10  # (seconds) time limit for each command
KILL_SWITCH_COMMANDS = ["!killpokemon"]  # must be all lowercase

# Keymap for Windows
windowsKeyMap = {
    "up": win32con.VK_UP,
    "left": win32con.VK_LEFT,
    "down": win32con.VK_DOWN,
    "right": win32con.VK_RIGHT,
    "a": ord("X"),
    "b": ord("Z"),
    "l": ord("A"),
    "r": ord("S"),
    "start": ord("E"),
    "select": ord("G"),
}

# Keymap for Linux, if you're using Windows you can ignore this
linuxKeyMap = {
    "up": "Up",
    "left": "Left",
    "down": "Down",
    "right": "Right",
    "a": "x",
    "b": "z",
    "l": "a",
    "r": "s",
    "start": "s",
    "select": "e",
}
###


async def main():
    if CHANNEL_NAME == "CHANNEL_NAME":
        print("Please set the CHANNEL_NAME variable in the main.py file")
    else:
        os_type = platform.system()

        keymap = windowsKeyMap if os_type == "Windows" else linuxKeyMap

        twitchPlaysX = TwitchPlaysX(
            KEY_DURATION, KEY_DELAY, keymap, CHANNEL_NAME, X_LIMIT, KILL_SWITCH_COMMANDS
        )

        print(f"Starting TwitchPlaysX for channel: {CHANNEL_NAME}")
        await twitchPlaysX.play()


if __name__ == "__main__":
    asyncio.run(main())
