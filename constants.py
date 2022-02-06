import os
from dotenv import load_dotenv

# from dataclasses import dataclass  # TODO?

from util import StringEnum, IntEnum


load_dotenv()


class TextChatIds(IntEnum):
    SCRIBBLIO = int(os.getenv("TEXT_CHAT_ID_SCRIBBLIO"))
    ANIMALS = int(os.getenv("TEXT_CHAT_ID_ANIMAL"))
    TEST = int(os.getenv("TEXT_CHAT_ID_TEST"))
    ADMIN = int(os.getenv("TEXT_CHAT_ID_ADMIN"))


class Tokens(StringEnum):
    DISCORD = os.getenv("DISCORD_TOKEN")
    GOOGLE = os.getenv("GOOGLE_TOKEN")


class Emojis(StringEnum):
    UPVOTE = "👍"
    DOWNVOTE = "👎"
    STOP = "🛑"


class Commands:
    class Scribblio(StringEnum):
        EXPORT = "!export"
        ADD = "!add"

    class Animals(StringEnum):
        ANIMAL = "!ambimal"

        # TODO
        # DACHSHUND = "!dachshund"
        # SHIB = "!shib"
        # CAT = "!cat"

    class Admin(StringEnum):
        UPDATE_IMAGES = "!update_images"
        # DELETE_OLD_IMAGES = "TODO"
        # TODO update single topic?


# just for ids, get any other info from the user object from discord
class Users(IntEnum):
    DISCORD_BOT = int(os.getenv("USER_ID_DISCORD_BOT"))
    ME = int(os.getenv("USER_ID_ME"))
