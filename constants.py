import os
from dotenv import load_dotenv

from util import StringEnum, IntEnum


load_dotenv()


class TextChatIds(IntEnum):
    SCRIBBLIO = int(os.getenv("TEXT_CHAT_ID_SCRIBBLIO"))
    ANIMALS = int(os.getenv("TEXT_CHAT_ID_ANIMAL"))
    TEST = int(os.getenv("TEXT_CHAT_ID_TEST"))


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
        SHIB = "!shib"
        CAT = "!cat"
        DOG = "!doggo"


# just for ids, get any other info from the user object from discord
class Users(IntEnum):
    DISCORD_BOT = int(os.getenv("USER_ID_DISCORD_BOT"))
    ME = int(os.getenv("USER_ID_ME"))