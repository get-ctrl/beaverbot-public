

import asyncio
import requests
import random
import json

from discord import DiscordBot
from discordmeta import Meta, Message, Author

BOT_TOKEN = ""

BEAVER_GIFS = [
    "https://tenor.com/view/beaver-carrot-eating-gif-21665554",
    "https://tenor.com/view/beaver-beaver-walk-beaver-hug-gif-3230734869832725232",
    "https://tenor.com/view/beaver-biting-tree-gif-5027262107110099517",
    "https://tenor.com/view/beaver-belly-cleaning-fat-gif-13239047136298053675",
    "https://tenor.com/view/beaver-bober-gif-10382563910831956595",
    "https://tenor.com/view/beaver-carrying-hurry-%D0%B1%D0%BE%D0%B1%D0%B5%D1%80-carrots-gif-25255221",
    "https://tenor.com/view/tulip-beaver-scratching-hotseventyfive-cute-gif-4741940090082318002",
    "https://tenor.com/view/beaver-silent-beaver-silentbeaver-cute-beaver-beaver-cute-gif-2665101477743541514",
]

HTTP_REPLY = {
    "content": "",
    "nonce": None,
    "tts": False,
    "message_reference":{
    },
    "allowed_mentions":{
        "parse":[
            "users",
            "roles",
            "everyone"
            ],
        "replied_user": True
    },
    "flags":0
}

http = requests.Session()
http.headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
}

async def reply(msg, content):
    data = HTTP_REPLY.copy()
    if msg.guild_id:
        data["message_reference"]["guild_id"] = msg.guild_id
    data["message_reference"]["channel_id"] = msg.channel_id
    data["message_reference"]["message_id"] = msg.id
    data["content"] = content
    url = "https://discord.com/api/v9/channels/{0}/messages".format(msg.channel_id)
    req = http.post(url, data=json.dumps(data))
    return req

async def on_message_create(meta):
    msg = Message(meta)
    if msg.content.startswith("!beaver"):
        await reply(msg, random.choice(BEAVER_GIFS))
        return
    if random.randrange(0,10) == 5:
        await reply(msg, random.choice(BEAVER_GIFS))
        return

async def main():
    bot = DiscordBot(BOT_TOKEN)
    bot.events = {"MESSAGE_CREATE": [on_message_create]}
    await bot.start()
    print("ok")

asyncio.run(main())
