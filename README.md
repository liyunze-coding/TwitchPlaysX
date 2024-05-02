# Twitch Plays X (by RythonDev)

> (Credits to [TwitchPlaysPokemon] and [TwitchPlayX by hzoo](https://github.com/hzoo/TwitchPlaysX))

Allows your Twitch chat to play games such as Pokemon!

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)
![Windows 11 Badge](https://img.shields.io/badge/Windows%2011-0078D4?logo=windows11&logoColor=fff&style=for-the-badge)
![Linux Badge](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=000&style=for-the-badge)

## How it works

1. Connects to your Twitch chat
2. Reads messages
3. Check if messages contains controls only: 
   - `up up down down left right` - pass
   - `what's up` - fail
4. Executes keyboard controls

## Installation

1. Install [Python](https://python.org) onto your machine
2. Download zip file or Clone the repo via:
    ```
    git clone https://github.com/liyunze-coding/TwitchPlaysX.git
    ```

3. Modify `CHANNEL_NAME` in `main.py`:
    ``` 
    CHANNEL_NAME = "rythondev"
    ```

4. Install the requirements:

    Windows:
    ```
    pip install pywin32
    ```

    Linux:
    ```
    sudo apt-get install xdotool
    ```

5. Run the script:
    ```
    py main.py
    ```