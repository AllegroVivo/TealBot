import os

from discord    import Intents
from dotenv     import load_dotenv

from classes.bot    import TealBot
################################################################################

bot = TealBot(
    description="FrogBot is Best!",
    intents=Intents.default(),
    debug_guilds=[389751128784502785, 303742308874977280, 955933227372122173]
)

################################################################################

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

################################################################################

load_dotenv()

bot.run(os.getenv("DISCORD_TOKEN"))

################################################################################
