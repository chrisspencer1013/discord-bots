# discord bot
#
# TODO:
# - word similarity deduping? (or atleast logging)
# - weeb bot
#   - google sheets integration
#   - weighting (recent is lower, votes are higher)
# https://developers.google.com/sheets/api/quickstart/python
import os
import re
import logging

import discord
from discord.ext import commands

import google_helper
from constants import TextChatIds, Tokens, Emojis, Commands, Users


logging.basicConfig(level=logging.INFO)


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


async def export_phrases(context):
    channel = context.channel
    messages = await context.channel.history().flatten()
    phrases = []
    for message in messages:
        command, arg = prep_command(message.content)
        clean_msg = clean_message(arg)

        upvotes, downvotes = get_votes(message)

        if (
            command == Commands.Scribblio.ADD
            and upvotes >= downvotes
            and len(clean_msg) < 30
            and len(clean_msg) != 0
        ):
            phrases.append(clean_msg)

    phrases = list(set(phrases))
    phrases_str = ", ".join(phrases)
    summary = f"# phrases: {len(phrases)} \n# chars: {len(phrases_str)} \n"
    await channel.send(summary + "```" + phrases_str + "```")


@client.event
async def on_message(context):
    channel = context.channel
    command, arg = prep_command(context.content)
    if command is not None:
        logging.info(f"command: `{command}`, arg: `{arg}`")
    else:
        logging.info(f"message: `{arg}`")

    if context.author.id == Users.DISCORD_BOT:
        # Don't process any messages the bot creates
        return

    # need this for client.commands to work with on message too
    # await client.process_commands(context)
    if context.channel.id == TextChatIds.SCRIBBLIO:
        if command == Commands.Scribblio.EXPORT:
            await export_phrases(context)
        elif command == Commands.Scribblio.ADD:
            if len(arg) > 29 or len(arg) == 0:
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
    logging.info(f"{client.user} has connected to Discord!")


client = commands.Bot(command_prefix="!")
client.run(Tokens.DISCORD)
