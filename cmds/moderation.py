import discord
from discord import app_commands
from discord.ext import commands
import utils.db as db
import time
import re
import datetime
from typing import Literal
from utils import utils

class moderation(commands.Cog):
	@app_commands.command()
	@app_commands.describe(victim="Member to sanction")
	@app_commands.describe(severity="Type of sanction")
	@app_commands.describe(duration="Time of mute (eg: 1s for 1 second, 1m for 1 minute, 1h for 1 hour, 1d for 1 day.)")
	@app_commands.describe(reason="Reason of mute")
	@app_commands.rename(victim='member')
	async def mute(self,interaction: discord.Interaction, victim: discord.Member, severity: Literal['S2', 'N/A'], duration: str, reason: str):
		try:
			guild_id = interaction.guild.id
			user_id = victim.id
			moderator_id = interaction.user.id
			duration_delta = utils.parse_duration(duration)
			await victim.timeout(duration_delta, reason=f"{reason} - {interaction.user.name}", )
			await interaction.response.send_message(f"Moderation `{db.insert_moderation(guild_id=guild_id, user_id=user_id, moderator_id=moderator_id, moderation_type=reason, severity=severity, duration=duration, time=str(time.time()))}`: Muted <@{user_id}> for {duration}: **{severity}. {reason}**")
		except Exception as e:
			await interaction.response.send_message("Unhandled exception caught:\n```\n{e}\n```", ephemeral=True)

async def setup(client):
	await client.add_cog(moderation(client))