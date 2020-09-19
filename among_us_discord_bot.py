import re
import subprocess
import asyncio
import discord
from time import time
import commentjson

client = discord.Client()

try:
    json_file = open("AmongUsDB.json")
except FileNotFoundError:
    json_file = open("AmongUsDB.json.json")

file_data = commentjson.load(json_file)
json_file.close()

print("Settings from file:", file_data)

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

async def controller():
    await client.wait_until_ready()
    detection_cooldown = 0

    channel_voice_id = int(file_data["discord"]["channel_voice_id"])
    meeting_end_mute_delay = int(file_data["preferences"]["meeting_end_mute_delay"])
    game_start_mute_delay = int(file_data["preferences"]["game_start_mute_delay"])

    tshark_location = file_data["settings"]["tshark_location"]
    interface = file_data["settings"]["interface"]
    server_port = int(file_data["settings"]["server_port"])
    client_port = file_data["settings"]["client_port"]
    if client_port != "":
        client_port = int(client_port)
    delay_between_mutes = float(file_data["settings"]["delay_between_mutes"])

    voice_channel = client.get_channel(channel_voice_id)

    mute_action = 1 # 0 - mute | 1 - unmute
    mute_time = 1

    log_format = '-e "data.data" -e "udp.srcport" -e "udp.dstport" -e "udp.time_relative"'
    command = f'{tshark_location} -i {interface} -T fields {log_format} -Y "udp"'
    print("command:", command)

    for line in execute(command):
        if "0" in line:
            args = line[:-1].split('\t')

            hexdata = args[0]
            rawdata = bytes.fromhex(hexdata)
            srcport = args[1]
            dstport = args[2]
            # time_ = args[3]

            if (int(srcport) == server_port or int(dstport) == server_port) and \
                (client_port == "" or (int(srcport) == client_port or int(dstport) == client_port)):
                if len(rawdata)>4 and (time()-detection_cooldown > 5):
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
                        regex = re.search("^(01).{6}(0005).{6}(80)(02|03)(0002).{2}(16|0116)", hexdata)
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

            if mute_time != 0 and mute_time <= time():
                mute_time = 0
                for member in voice_channel.members:
                    try:
                        await member.edit(mute=(not bool(mute_action)))
                    except:
                        print("Doesn't have permissions to mute users. (or an error)")

                    await asyncio.sleep(delay_between_mutes)

                try:
                    await voice_channel.set_permissions(voice_channel.guild.default_role, connect=bool(mute_action))
                except:
                    print("Doesn't have permissions to change if users can connect to the voice channel. (or an error)")

                print("mute action:", mute_action, bool(mute_action))

client.loop.create_task(controller())
client.run(file_data["discord"]["token"])


## Trash

# @client.event
# async def on_ready():
#     print("Discord bot is ready")


# f'{tshark_path} -i {interface} -T fields -Y "{filter_}" {log_format}'