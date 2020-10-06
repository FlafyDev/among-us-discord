import nest_asyncio
nest_asyncio.apply()
import commentjson
import bot_discord
import os

def load_json():
    global settings
    try:
        json_file = open("settings.json", encoding="utf8")
    except FileNotFoundError:
        json_file = open("settings.json.json", encoding="utf8")

    settings_data = commentjson.load(json_file)
    json_file.close()
    print("Settings from file:", settings_data)

    class Settings:
        def __init__(self, json_data):
            self.bot_server_port = json_data["settings"]["bot_server_port"]
            if self.bot_server_port == "":
                self.bot_server_port = int(os.environ['PORT'])
            else:
                self.bot_server_port = int(self.bot_server_port)
            self.bot_server_url = json_data["settings"]["bot_server_url"]

            self.bot_token = json_data["discord"]["token"]
            self.room_creation_voice_id = json_data["discord"]["room_creation_voice_id"]
            self.general_voice_id = json_data["discord"]["general_voice_id"]
            self.room_category_id = int(json_data["discord"]["room_category_id"])
            self.max_users_in_room = int(json_data["discord"]["max_users_in_room"])
            self.room_prefix = json_data["discord"]["room_prefix"]

            if self.general_voice_id != "":
                self.general_voice_id = int(self.general_voice_id)
            if self.room_creation_voice_id != "":
                self.room_creation_voice_id = int(self.room_creation_voice_id)


    settings = Settings(settings_data)

settings = None
load_json()

def load_embeds():
    global embeds
    try:
        json_file = open("embeds.json", encoding="utf8")
    except FileNotFoundError:
        json_file = open("embeds.json.json", encoding="utf8")

    embeds = commentjson.load(json_file)
    json_file.close()
    print("Embeds from file:", embeds)

embeds = None
load_embeds()

print("Waiting for the Discord bot and the server to ready...")
bot_discord.run_discord(settings, embeds)