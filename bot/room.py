import asyncio
import base64
import random
import string
from discord.member import Member
from discord.ext.commands import Bot
import bot_discord
from time import time

accepted_characters = string.digits + string.ascii_letters + " "
rooms = {}

class Room(object):
    def __init__(self, owner: Member, settings, client: Bot):
        global rooms

        self.loop = asyncio.get_running_loop()
        self.settings = settings
        self.voice = None
        self.owner = owner
        self.owner_name = ''.join([letter if letter in accepted_characters else '' for letter in self.owner.name])
        if len(self.owner_name.strip()) == 0:
            self.owner_name = "Player"
        self.client = client
        self.secret_key = None
        self.mute = 0
        self.room_code = ""

        if owner.id in rooms:
            raise RoomAlreadyExistsException()

        if owner.voice is None:
            raise UserNotInVoiceException()

        if bot_discord.channels.room_creation_voice is not None and owner.voice.channel != bot_discord.channels.room_creation_voice:
            raise UserNotInRoomCreationVoiceException()

        self.voice = self.loop.run_until_complete(bot_discord.channels.room_category.create_voice_channel(self.get_name(), user_limit=settings.max_users_in_room))
        self.loop.run_until_complete(self.owner.move_to(self.voice))
        self.loop.run_until_complete(self.generate_secret())
        rooms.update({owner.id: self})

    async def close(self):
        global rooms

        if bot_discord.channels.general_voice is not None:
            await bot_discord.move_users(self.voice, bot_discord.channels.general_voice)
            # for member in self.voice.members:
            #     await member.move_to(bot_discord.channels.general_voice)

        await self.voice.delete()
        del rooms[self.owner.id]

    async def generate_secret(self):
        self.secret_key = base64.b64encode(''.join(random.choice(string.ascii_letters)
            for _ in range(8)).encode("utf-8")).decode("utf-8")

        await self.owner.send(f"Your room's key is ```{self.generate_code_for_client()}```"
                              f"\nPut it in your client to mute automatically.\n")

    def get_name(self):
        return f"{self.settings.room_prefix}" \
               f"{self.room_code + ('' if self.room_code == '' else '-')}" \
               f"{self.owner.name}"

    async def refresh(self):
        print(int(time()), "-- in refresh")
        for member in self.voice.members:
            await bot_discord.mute_member(member, self.mute)
        print(int(time()), "-- done refresh")

    def generate_code_for_client(self):
        return base64.b64encode(f"{self.settings.self.bot_server_url}$".encode("utf-8"))\
            .decode("utf-8") + self.secret_key

    async def set_code(self, room_code: str):
        print("Setting room code", room_code)
        if len(room_code) == 6:
            for letter in room_code:
                if letter not in string.ascii_letters:
                    return

            self.room_code = room_code
            await self.voice.edit(name=self.get_name())

class RoomAlreadyExistsException(Exception):
    pass

class UserNotInVoiceException(Exception):
    pass

class UserNotInRoomCreationVoiceException(Exception):
    pass
