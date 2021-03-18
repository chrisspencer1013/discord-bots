# discord bot
import os
import re
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

from util import StringEnum, IntEnum

load_dotenv()
client = commands.Bot(command_prefix="!")

TOKEN = os.getenv("DISCORD_TOKEN")
SCRIBBLIO_TEXT_CHAT_ID = os.getenv("SCRIBBLIO_TEXT_CHAT_ID")


class Emojis(StringEnum):
    UPVOTE = "👍"
    DOWNVOTE = "👎"
    STOP = "🛑"


class Commands(StringEnum):
    EXPORT = "!export"
    ADD = "!add"


# just for ids, get any other info from the user object from discord
class Users(IntEnum):
    SCRIBBLIO_BOT = os.getenv("USER_ID_SCRIBBLIO_BOT")
    ME = os.getenv("USER_ID_ME")


def prep_command(message_content):
    message = str(message_content).strip()
    if message.startswith("!"):
        command = message.split(" ")[0].lower()
        args = message.lstrip(command).strip()
    else:
        command = None
        args = message
    return command, args


regex_pattern = re.compile("[^a-zA-Z0-9 #$%&'()*+\-./:;<=>?!@\[\]^_{|}~\"]+")


def clean_message(message_content):
    return str(regex_pattern.sub("", message_content)).strip()


def get_votes(message):
    upvotes = downvotes = 0
    for reaction in message.reactions:
        if reaction.emoji == Emojis.UPVOTE:
            upvotes = reaction.count
        elif reaction.emoji == Emojis.DOWNVOTE:
            downvotes = reaction.count
    return upvotes, downvotes


def export_phrases(context):
    channel = context.channel
    messages = await context.channel.history().flatten()
    phrases = []
    for message in messages:
        command, arg = prep_command(message.content)
        clean_msg = clean_message(arg)

        upvotes, downvotes = get_votes(message)

        if command == Commands.ADD and upvotes >= downvotes and len(clean_msg) < 30:
            phrases.append(clean_msg)

    phrases = list(set(phrases))
    await channel.send("```" + ", ".join(phrases) + "```")


@client.event
async def on_message(context):
    channel = context.channel
    command, arg = prep_command(context.content)
    logging.info(f"command: \n\t`{command}`, arg: \n\t`{arg}`")

    if context.author.id == Users.SCRIBBLIO_BOT:
        # Don't process any messages the bot creates
        return

    # need this for client.commands to work with on message too
    # await client.process_commands(context)

    if context.channel.id == SCRIBBLIO_TEXT_CHAT_ID:
        if command == Commands.EXPORT:
            export_phrases(context)
        elif command == Commands.ADD:
            if len(arg) > 29:
                await context.add_reaction(Emojis.STOP)
            else:
                await context.add_reaction(Emojis.UPVOTE)
                await context.add_reaction(Emojis.DOWNVOTE)
        elif command == "!purge":
            if context.author.id == Users.ME:
                pass
                # await context.channel.purge(limit=50, oldest_first=True)
            else:
                await channel.send("lol no")


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


client.run(TOKEN)