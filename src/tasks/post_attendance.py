import datetime
import json
import logging

import discord
from discord.ext import commands, tasks

from config import config
from db.models import get_last_posted_date, set_last_posted_date

logger = logging.getLogger(__name__)


def load_training_data():
    with open("trainings.json", "r") as f:
        return json.load(f)


class AttendanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.post_training_task.cancel()

    async def post_training(self):
        current_date = datetime.datetime.now(datetime.timezone.utc).date()
        last_posted = get_last_posted_date()
        logger.info(
            f"Checking training posts. Last posted: {last_posted}, Current: {current_date}"
        )

        if last_posted and last_posted >= current_date:
            logger.info("Already posted today, skipping")
            return

        data = load_training_data()

        tomorrow_date = current_date + datetime.timedelta(days=1)
        tomorrow_day = tomorrow_date.strftime("%A")
        tomorrows_training_sessions = []

        for training_type in ["indoor", "outdoor"]:
            start_date = datetime.date.fromisoformat(data[training_type]["start_date"])
            end_date = datetime.date.fromisoformat(data[training_type]["end_date"])

            if start_date <= tomorrow_date <= end_date:
                sessions = data[training_type]["training_sessions"].get(
                    tomorrow_day, []
                )
                tomorrows_training_sessions.extend(sessions)

        if not tomorrows_training_sessions:
            logger.info(
                f"No training sessions scheduled for {tomorrow_day} ({tomorrow_date})"
            )
            set_last_posted_date(current_date)
            return

        attendance_channel = self.bot.get_channel(config.ATTENDANCE_CHANNEL_ID)

        for training_session in tomorrows_training_sessions:
            logger.info(
                f"Posting session: {training_session['name']} at {training_session['time']}"
            )
            embed = discord.Embed(
                title=f"{tomorrow_day} {training_session['name']}",
                colour=discord.Colour.random(),
            )
            embed.add_field(
                name="Date", value=tomorrow_date.strftime("%d/%m/%y"), inline=True
            )
            embed.add_field(name="Time", value=training_session["time"], inline=True)
            embed.add_field(
                name="Location", value=training_session["location"], inline=True
            )
            await attendance_channel.send(embed=embed)

        logger.info("Successfully posted all training sessions")
        set_last_posted_date(current_date)

    @tasks.loop(time=datetime.time(hour=18, tzinfo=datetime.timezone.utc))
    async def post_training_task(self):
        await self.post_training()

    @post_training_task.error
    async def post_training_error(self, error):
        logger.error(f"Error in post_training task: {str(error)}", exc_info=error)

    @commands.Cog.listener()
    async def on_ready(self):
        current_time = datetime.datetime.now(datetime.timezone.utc).time()
        if current_time >= datetime.time(17, 0, 0):
            await self.post_training()
        self.post_training_task.start()


async def setup(bot):
    await bot.add_cog(AttendanceCog(bot))
