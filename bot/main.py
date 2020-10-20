import nest_asyncio
nest_asyncio.apply()
import commentjson
import bot_discord
import os
import dotenv
dotenv.load_dotenv()

def load_json():
    global settings
    try:
        json_file = open("settings.json", encoding="utf8")
    except FileNotFoundError:
        json_file = open("settings.json.json", encoding="utf8")

    settings_data = commentjson.load(json_file)
    json_file.close()
    print("settings.json:", settings_data)

    class Settings:
        def __init__(self, json_data):
            self.bot_server_port = os.environ.get("BOT_SERVER_PORT")
            if self.bot_server_port == "":
                self.bot_server_port = int(os.environ['PORT'])
            else:
                self.bot_server_port = int(self.bot_server_port)
            self.bot_server_url = os.environ.get("BOT_SERVER_URL")

            self.bot_token = os.environ.get("BOT_TOKEN")
            self.room_creation_voice_id = os.environ.get("ROOM_CREATION_VOICE_ID")
            self.general_voice_id = os.environ.get("GENERAL_VOICE_ID")
            self.room_category_id = int(os.environ.get("ROOM_CATEGORY_ID"))
            self.room_creation_role = os.environ.get("ROOM_CREATION_ROLE")

            self.max_users_in_room = int(json_data["max_users_in_room"])
            self.room_prefix = json_data["room_prefix"]

            if self.general_voice_id.strip() != "":
                self.general_voice_id = int(self.general_voice_id)
            if self.room_creation_voice_id.strip() != "":
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
