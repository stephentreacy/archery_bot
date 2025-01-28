import logging

import discord
from discord import app_commands
from discord.ext import commands

from config import config
from db.models import Session, User

logger = logging.getLogger(__name__)


class AddInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(
            self.add_info, guild=discord.Object(id=config.GUILD_ID)
        )

    @app_commands.command(name="add_info", description="Add your IDs to the database")
    async def add_info(
        self, interaction: discord.Interaction, student_id: str, archery_ireland_id: str
    ):
        discord_id = str(interaction.user.id)
        session = Session()
        user = session.query(User).filter_by(discord_id=discord_id).first()
        if user:
            user.student_id = student_id
            user.ai_id = archery_ireland_id
            message = "Your information has been updated in the database."
        else:
            new_user = User(
                discord_id=discord_id, student_id=student_id, ai_id=archery_ireland_id
            )
            session.add(new_user)
            message = "Your information has been added to the database."

        session.commit()
        logger.info(
            f"User {interaction.user.name} added/updated their info to the database."
        )
        await interaction.response.send_message(message, ephemeral=True)


async def setup(bot):
    await bot.add_cog(AddInfo(bot))
