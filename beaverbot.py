

import asyncio
import random

from discord import (
    Meta,
    Author,
    Message,
    DiscordBot
)

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

bot = DiscordBot(BOT_TOKEN)

async def on_message_create(meta):
    msg = Message(meta)
    if random.randint(0,10) == 5:
        await bot.reply(msg, random.choice(BEAVER_GIFS))

async def cmd_beaver(msg):
    await bot.reply(msg, random.choice(BEAVER_GIFS))

bot = DiscordBot(BOT_TOKEN)
bot.events = {"MESSAGE_CREATE": [on_message_create]}
bot.commands = {
    "beaver": cmd_beaver
}

asyncio.run(bot.start())
