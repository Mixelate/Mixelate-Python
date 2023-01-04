import discord
import time
import yaml
from discord import app_commands
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

launch_time = datetime.utcnow()

class UtilsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="latency", description="View the bot's latency!")
    async def latency(self, interaction: discord.Interaction) -> None:
        latency = round(self.bot.latency)
        await interaction.response.send_message(f'{latency}ms', ephemeral=True)

    @app_commands.command(name="ping", description="View the bot's ping!")
    async def ping(self, interaction: discord.Interaction) -> None:
        start = time.perf_counter()
        await interaction.response.send_message("Pinging...", ephemeral=True)
        end = time.perf_counter()
        duration = (end - start) * 1000
        await interaction.edit_original_response(content='Pong! {:.2f}ms'.format(duration))

    @app_commands.command(name="uptime", description="View the bot's uptime!")
    @app_commands.guilds(discord.Object(id=1027020838714740777))
    async def uptime(self, interaction: discord.Interaction) -> None:
        delta_uptime = datetime.utcnow() - launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await interaction.response.send_message(f"{days}d, {hours}h, {minutes}m, {seconds}s", ephemeral=True)

async def setup(bot):
    await bot.add_cog(UtilsCog(bot), guilds=[discord.Object(id=guild_id)])