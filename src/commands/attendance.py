import logging
from io import BytesIO

import discord
from discord import app_commands
from discord.ext import commands
from openpyxl import Workbook

from config import config
from db.models import User

logger = logging.getLogger(__name__)


class Attendance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name="Get Attendance Excel",
                callback=self.get_attendance_excel,
            ),
            guild=discord.Object(id=config.GUILD_ID),
        )

    async def get_attendance_excel(
        self, interaction: discord.Interaction, message: discord.Message
    ):
        # Command only usable by committee members
        user_roles = [role.id for role in interaction.user.roles]
        if config.COMMITTEE_ROLE_ID not in user_roles:
            await interaction.response.send_message(
                "You do not have the required role to use this command.", ephemeral=True
            )
            return

        # Command should only be used in the attendance channel
        if interaction.channel_id != config.ATTENDANCE_CHANNEL_ID:
            await interaction.response.send_message(
                "This command can't be used outside of #attendance.", ephemeral=True
            )
            return

        # Buys the bot more time to respond, up to 15 minutes
        await interaction.response.defer(ephemeral=True)

        reactions = message.reactions

        discord_ids = set()
        user_id_names = {}
        for reaction in reactions:
            async for user in reaction.users():
                user_id = str(user.id)
                discord_ids.add(user_id)
                user_id_names[user_id] = user.name

        student_ids = User.get_student_ids(list(discord_ids))
        logger.info(f"Retrieved {len(student_ids)} Student IDs from DB: {student_ids}")

        retrieved_discord_ids = set(student_ids.keys())
        missing_ids = discord_ids - retrieved_discord_ids
        for user_id in missing_ids:
            logging.info(
                f"User {user_id_names[user_id]} does not have a student ID in the database."
            )

        # Create an Excel file
        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance"

        for student_id in student_ids.values():
            ws.append([student_id])

        file_stream = BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)
        excel_file = discord.File(file_stream, filename="attendance.xlsx")

        await interaction.followup.send(
            "Here are the student IDs of users who reacted:",
            file=excel_file,
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Attendance(bot))
