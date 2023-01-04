import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class ReferalsCog(commands.GroupCog, name="referals"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="earned", description="View your income from referals!")
    async def earned(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="generate", description="Generate a referal link!")
    async def generate(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="active", description="Displays all active referals!")
    async def active(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

class ReferalsReferalsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="referals", description="Opens the Referals GUI!")
    async def referalsreferals(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReferalsCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(ReferalsReferalsCog(bot))