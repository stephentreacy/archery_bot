import discord
from discord import app_commands
from discord.ext import commands

from config import config


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.hello, guild=discord.Object(id=config.GUILD_ID))

    @app_commands.command(name="hello", description="Say hello!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Hello(bot))
