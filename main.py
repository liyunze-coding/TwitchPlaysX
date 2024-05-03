import win32con  # Windows only
from functions import TwitchPlaysX
import platform
import asyncio

# SETTINGS
CHANNEL_NAME = "RythonDev"
KEYDELAY = 0.3
X_LIMIT = 10  # "up20" will be converted to "up10" if X_LIMIT is 10

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
    "start": ord("S"),
    "select": ord("E"),
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

        twitchPlaysX = TwitchPlaysX(KEYDELAY, keymap, CHANNEL_NAME, X_LIMIT)

        print(f"Starting TwitchPlaysX for channel: {CHANNEL_NAME}")
        await twitchPlaysX.listen()


if __name__ == "__main__":
    asyncio.run(main())
