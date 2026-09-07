

import asyncio
import random

from discord import (
    Meta,
    Author,
    Message,
    DiscordBot
)

BOSNA_ID = "1443818584391553144"

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
    "https://giphy.com/gifs/pbs-beavers-1FJayrPE7XGDe",
    "https://giphy.com/gifs/cbc-animals-aww-hello-spring-W2c7mqWdT4q87pK9bD",
    "https://giphy.com/gifs/pbsnature-animals-nature-beaver-zH9uwKBgRD6AtGqX6K",
    "https://giphy.com/gifs/sandiegozoo-nk2C49mUNljb1scZgY",
    "https://giphy.com/gifs/eating-beaver-sweet-potato-vUOmoWD8P7IRW8a4x7",
    "https://giphy.com/gifs/pbs-nature-the-american-southwest-WbtTI1gpW2hQ2CjNES"
]

bot = DiscordBot(BOT_TOKEN)

async def on_message_annoybosna(meta):
    msg = Message(meta)
    if msg.author.id == BOSNA_ID:
        await bot.reply(msg, random.choice(BEAVER_GIFS))

async def on_message_create(meta):
    msg = Message(meta)
    if random.randint(0,10) == 5:
        await bot.reply(msg, random.choice(BEAVER_GIFS))

async def cmd_beaver(msg):
    await bot.reply(msg, random.choice(BEAVER_GIFS))

async def cmd_info(msg):
    data = """
client = {0}
interval = {1}
sequence = {2}
http = {3}
""".format(bot.client, bot.heartbeat_interval, bot.heartbeat_sequence, bot.http)
    await bot.reply(msg, data)

bot = DiscordBot(BOT_TOKEN)
bot.events = {"MESSAGE_CREATE": [on_message_create,on_message_annoybosna]}
bot.commands = {
    "beaver": cmd_beaver,
    "info": cmd_info
}

asyncio.run(bot.start())
