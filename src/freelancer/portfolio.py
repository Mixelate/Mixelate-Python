import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class PortfolioCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="portfolio", description="View a user's portfolio!")
    @app_commands.describe(user="Who's profile would you like to view?")
    async def portfolio(self, interaction: discord.Interaction, user: discord.Member) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message('That user does not have any information to view!', ephemeral=True)
        else:
            if a[4] == 'null':
                portfolio = "N/A"
            else:
                portfolio = a[4]
            embed = discord.Embed(
                title="",
                description=f"**{portfolio}**",
                color=discord.Color.from_str(embed_color))
            embed.set_author(name=f"{user.name}'s Portfolio", icon_url=user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(PortfolioCog(bot), guilds=[discord.Object(id=guild_id)])