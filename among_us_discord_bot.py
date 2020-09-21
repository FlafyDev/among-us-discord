from time import time, sleep
import commentjson
import threading
import asyncio
import discord
import pyshark
import re

try:
    json_file = open("AmongUsDB.json")
except FileNotFoundError:
    json_file = open("AmongUsDB.json.json")

file_data = commentjson.load(json_file)
json_file.close()
print("Settings from file:", file_data)

discord_ready = False
discord_mute_voice_chat = None
discord_voice_channel = None
discord_mute_member = None
discord_loop = None

def runDiscord():
    global discord_loop
    discord_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(discord_loop)
    client = discord.Client()

    async def mute_voice_chat(voice_chat, mute_action):
        try:
            await voice_chat.set_permissions(discord_voice_channel.guild.default_role, connect=bool(mute_action))
        except Exception as e:
            print("Doesn't have permissions to change if users can connect to the voice channel. (or an error)", e)
        pass

    async def mute_member(member, mute_action):
        try:
            await member.edit(mute=(not bool(mute_action)))
        except Exception as e:
            print("Doesn't have permissions to mute/unmute users. (or an error)", e)

    @client.event
    async def on_ready():
        global discord_ready, discord_mute_voice_chat, discord_voice_channel, discord_mute_member

        discord_mute_voice_chat = mute_voice_chat
        discord_mute_member = mute_member
        channel_voice_id = int(file_data["discord"]["channel_voice_id"])
        discord_voice_channel = client.get_channel(channel_voice_id)

        print("Bot is ready")
        discord_ready = True

    client.run(file_data["discord"]["token"])

discord_thread = threading.Thread(target=runDiscord)
discord_thread.daemon = False
discord_thread.start()

def main():
    print("in main")
    while not discord_ready:
        sleep(0.5)

    meeting_end_mute_delay = int(file_data["preferences"]["meeting_end_mute_delay"])
    game_start_mute_delay = int(file_data["preferences"]["game_start_mute_delay"])

    tshark_location = file_data["settings"]["tshark_location"]
    interface = file_data["settings"]["interface"]
    server_port = int(file_data["settings"]["server_port"])
    client_port = file_data["settings"]["client_port"]
    if client_port != "":
        client_port = int(client_port)
    delay_between_mutes = float(file_data["settings"]["delay_between_mutes"])

    detection_cooldown = 0
    mute_action = 1 # 0 - mute | 1 - unmute
    mute_time = 1

    def mute_action_function():
        nonlocal mute_action, mute_time
        if mute_time != 0 and mute_time <= time():
            mute_time = 0
            for member in discord_voice_channel.members:
                asyncio.run_coroutine_threadsafe(discord_mute_member(member, mute_action), discord_loop).result()
                sleep(delay_between_mutes)

            asyncio.run_coroutine_threadsafe(discord_mute_voice_chat(discord_voice_channel, mute_action), discord_loop).result()

            print("mute action:", mute_action, bool(mute_action))

    mute_action_function()

    capture = pyshark.LiveCapture(interface=interface, tshark_path=tshark_location,
                                  display_filter=f"udp.port == {server_port} and data.len > 4 { '' if client_port == '' else 'and udp.port == '+str(client_port) }")

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

                    mute_time = time()+game_start_mute_delay
                    mute_action = 0
                    detection_cooldown = time()

            elif 16 >= len(rawdata) >= 15:
                regex = re.search("^(01).{6}(0005).{6}(80).{2}(0002)", hexdata)
                if regex is not None:
                    print("Meeting ended")

                    mute_time = time()+meeting_end_mute_delay
                    mute_action = 0
                    detection_cooldown = time()

            elif re.search("^(01).{6}(0005).*(401c460000401c46)", hexdata):
                print("Meeting started")

                mute_time = time()
                mute_action = 1
                detection_cooldown = time()

        mute_action_function()


main()
