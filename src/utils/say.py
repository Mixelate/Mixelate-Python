import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Literal, Optional

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class SayCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="say", description="Send a message from the bot!")
    @app_commands.describe(format="Do you want to send a plain or embedded message?")
    @app_commands.describe(message="What message do you want to send?")
    @app_commands.describe(title="What do you want the title of the embed to be (only for embeds)?")
    @app_commands.describe(role="What role do you want to ping?")
    async def say(self, interaction: discord.Interaction, format: Literal["Plain", "Embed"], message: str, title: Optional[str], role: Optional[discord.Role]) -> None:
        if format == "Plain":
            if role is None:
                await interaction.channel.send(message)
            else:
                await interaction.channel.send(f'{role.mention} \n \n{message}')
        if format == "Embed":
            if role is None:
                if title is None:
                    embed = discord.Embed(
                        description=message,
                        color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=title,
                        description=message,
                        color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(embed=embed)
            else:
                if title is None:
                    embed = discord.Embed(
                        description=message,
                        color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(content=role.mention, embed=embed)
                else:
                    embed = discord.Embed(title=title,
                        description=message,
                        color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(content=role.mention, embed=embed)
        await interaction.response.send_message('Sent!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(SayCog(bot), guilds=[discord.Object(id=guild_id)])