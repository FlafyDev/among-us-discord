from time import time, sleep
import commentjson
import threading
import asyncio
import discord
import pyshark
import re

def load_json():
    global settings
    try:
        json_file = open("AmongUsDB.json")
    except FileNotFoundError:
        json_file = open("AmongUsDB.json.json")

    settings_data = commentjson.load(json_file)
    json_file.close()
    print("Settings from file:", settings_data)

    class Settings:
        def __init__(self, json_data):
            self.meeting_end_mute_delay = int(json_data["preferences"]["meeting_end_mute_delay"])
            self.game_start_mute_delay = int(json_data["preferences"]["game_start_mute_delay"])
            self.tshark_location = json_data["settings"]["tshark_location"]
            self.interface = json_data["settings"]["interface"]
            self.server_port = int(json_data["settings"]["server_port"])
            self.client_port = json_data["settings"]["client_port"]
            if self.client_port != "":
                self.client_port = int(self.client_port)
            self.delay_between_mutes = float(json_data["settings"]["delay_between_mutes"])
            self.channel_voice_id = int(json_data["discord"]["channel_voice_id"])
            self.bot_token = json_data["discord"]["token"]
            self.unmute_users_on_other_channels = json_data["preferences"]["unmute_users_on_other_channels"]

    settings = Settings(settings_data)

settings = None
load_json()

discord_ready = False
discord_voice_channel = None
discord_mute_member = None
discord_loop = None

mute_action = 1  # 0 - mute | 1 - unmute
mute_time = 1

def runDiscord():
    global discord_loop
    discord_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(discord_loop)
    client = discord.Client()

    async def mute_member(member, mute_action_):
        try:
            await member.edit(mute=(not bool(mute_action_)))
        except Exception as e:
            print("Doesn't have permissions to mute/unmute users. (or an error)", e)

    @client.event
    async def on_voice_state_update(member, before, after):
        global mute_action
        if after.channel.id is not None:
            if after.channel.id == settings.channel_voice_id:
                await mute_member(member, mute_action)
            elif settings.unmute_users_on_other_channels:
                await mute_member(member, 1)

    @client.event
    async def on_ready():
        global discord_ready, discord_voice_channel, discord_mute_member

        discord_mute_member = mute_member
        discord_voice_channel = client.get_channel(settings.channel_voice_id)

        print("Bot is ready")
        discord_ready = True

    client.run(settings.bot_token)

discord_thread = threading.Thread(target=runDiscord)
discord_thread.daemon = False
discord_thread.start()

def mute_action_function():
    global mute_action, mute_time
    if mute_time != 0 and mute_time <= time():
        mute_time = 0
        for member in discord_voice_channel.members:
            asyncio.run_coroutine_threadsafe(discord_mute_member(member, mute_action), discord_loop).result()
            sleep(settings.delay_between_mutes)

        print("mute action:", mute_action, bool(mute_action))


def main():
    global mute_action, mute_time
    print("Waiting for bot to ready...")
    while not discord_ready:
        sleep(0.5)

    detection_cooldown = 0
    mute_action_function()
    capture = pyshark.LiveCapture(interface=settings.interface, tshark_path=settings.tshark_location,
                                  display_filter=f"udp.port == {settings.server_port} and data.len > 4 "
                                                 f"{ '' if settings.client_port == '' else 'and udp.port == '+str(settings.client_port) }")

    for packet in capture.sniff_continuously():
        hexdata = str(packet.data.data)
        rawdata = bytes.fromhex(packet.data.data)

        if time()-detection_cooldown >= 2:
            if ("EndGame".encode() in rawdata and rawdata[3:6] == bytes.fromhex("120005")) or (rawdata[3:6] == bytes.fromhex("060008")):
                print("Game ended")

                mute_time = time()
                mute_action = 1
                detection_cooldown = time()

            elif len(rawdata) >= 200:
                if "460000000001010101010101010101010101000000000" in hexdata:
                    print("Game started")

                    mute_time = time()+settings.game_start_mute_delay
                    mute_action = 0
                    detection_cooldown = time()

            elif 16 >= len(rawdata) >= 15:
                regex = re.search("^(01).{6}(0005).{6}(80).{2}(0002)", hexdata)
                if regex is not None:
                    print("Meeting ended")

                    mute_time = time()+settings.meeting_end_mute_delay
                    mute_action = 0
                    detection_cooldown = time()

            elif re.search("^(01).{6}(0005).*(401c460000401c46)", hexdata):
                print("Meeting started")

                mute_time = time()
                mute_action = 1
                detection_cooldown = time()

        mute_action_function()

main()
