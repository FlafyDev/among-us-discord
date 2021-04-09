# DEPRECATED 

---

# Flafy's Among Us Bot - BETA

<p align="center">
  <img src="icon-files/bot_icon_256.png">
</p>

**This is still in beta, so if you find any problems let me know.**  
This bot mutes discord users according to what happens in Among Us. It gets data from the game by the packets sent to/received from the server.

You can try the bot on a Discord server I created for this: https://discord.gg/Vh7VTWd  
The prefix for commands is `!au`

## Features
* Mutes and unmutes players according to what happens in Among Us(Doesn't mute dead players).
* Multiple games can run simultaneously and it's friendly with bigger servers(Wasn't tested yet).
* Everyone can start a voice channel for their game to play with anyone. No need for special permissions on the server
* Among Us codes will automatically be detected by the bot and will appear when doing `!au room invite/list` so you don't have to tell it whenever someone joins the voice channel.
* Safe server mutes. The bot uses server mutes to decide who will talk at any given time. There won't be any case where a user is server muted for no reason while the bot is running.

## How does it work
#### Room
A Room is a temporary voice channel that a user creates and owns until they leave it.  
A room has a maximum of 10 users.  
For how to use the rooms do: `!au help`
#### Client
###### Currently only tested on Windows.    
Only the owner of a room must use the client.  
The client is used for the bot to know what's going on in the game.  

Download link in [releases](https://github.com/FlafyDev/among-us-discord/releases)

![example image of the client](client_example.png)

## Hosting the bot - A Simple Step by Step Guide
### 1. Create the bot
1.1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications) and create a new application.  
1.2. Go to the "Bot" setting on the left side and add a bot.  
1.3. Now Go back to the first setting("General Information"), copy the "CLIENT ID" and paste it instead of the "CLIENTID" in the following URL `https://discord.com/api/oauth2/authorize?permissions=289410065&scope=bot&client_id=CLIENTID`  
1.4. Open the URL and add the bot to your server.
### 2. Hosting it on Heroku
2.1. Now the only thing left to do is to host it.  
Deploy the bot to Heroku with the button below.  
<a href="https://www.heroku.com/deploy/?template=https://github.com/FlafyDev/among-us-discord/tree/bot-only">
  <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy">
</a>  
Fill in all the information.  
2.2. After the bot is in your server, right-click the category you've specified as your "Room Category" and press on Edit Category, in the Permissions tab add the role the bot uses and enable the Connect permission.  
2.3. Done!
#### Notes:  
1. The bot's token can be obtained in the bot's application "Bot" setting(Like in step 1.2) 
2. To get IDs of categories, channels, and roles you need to go to your Discord's App Settings -> Appearance -> enable Developer Mode.
Now you'll be able to right-click on any of the three and select "Copy ID"

### More technical details
This bot was made in Python 3.9.0 and it runs a webserver to communicate with the user.

The `.env` file must be in the bot's folder and follow this format(without the commented lines). You will need to fill it correctly:
```
BOT_SERVER_PORT=8080                        # Set a port to run the webserver on. (blank for os.environ['PORT'])
BOT_SERVER_URL=http://localhost:8080/       # URL of the bot's web server to communicate with the user.
BOT_TOKEN=                                  # The Discord bot's token
ROOM_CREATION_VOICE_ID=voice_channel_id     # Users must be connected to this voice channel to create a room (blank for any voice)
GENERAL_VOICE_ID=voice_channel_id           # Will move the users to here before closing the room (blank for don't move)
ROOM_CATEGORY_ID=category_id                # Where voice channels for rooms will be created
ROOM_CREATION_ROLE=role_id                  # The role to tag when a room is created (Takes a role id, blank for don't tag)
```


The `settings.json` file must be in the bot's folder and should look like that:
```
{
  "max_users_in_room": 10, // 0 for unlimited users
  "room_prefix": "『\uD83D\uDD79』" // Voice channels' names will follow this format: f"{room_prefix}{room_owner}"
}
```

You DON'T have to build a special client to work with the bot.  

#### Permissions for the bot
The permissions the bot requires for Discord are: `Send Messages`, `Read Text Channels & See Voice Channels`,
`Manage Channels`, `Mute Members`, `Move Members`, `Create Invite` and `Manage Roles`. Or simply `permissions=289410065`.

The bot also needs the `Connect` permission in the category `room_category_id`. Right-click the category and click
`Edit Category`. In the `Permissions` tab add the role the bot uses and give it the `Connect` permission.

## Credits
Crewmate - https://github.com/MythicManiac/Crewmate

---
## Maybe in the future
* Only unmutes alive players when there is a meeting, ghosts(dead) players will remain muted till the game ends
* Tracks points for every imposter win(and maybe kill too?). Problems are that it can get competitive and it's easy to cheat
* Same bot for multiple servers. (Right now the bot only works in a single server)
