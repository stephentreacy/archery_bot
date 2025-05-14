import asyncio
import logging

import discord
from discord.ext import commands

from config import config
from db.models import setup_database

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True


client = commands.Bot(command_prefix="/", intents=intents)


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")
    guild = discord.Object(id=config.GUILD_ID)
    await client.tree.sync(guild=guild)


async def load_cogs():
    cogs = [
        "commands.add_info",
        "commands.hello",
        "commands.attendance",
        "tasks.post_attendance",
    ]
    for cog in cogs:
        await client.load_extension(cog)


async def main():
    setup_database(config.DATABASE_URL)
    await load_cogs()
    await client.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
