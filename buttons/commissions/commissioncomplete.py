import discord
import aiosqlite
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]

class TipLink(discord.ui.View):
    def __init__(self, tiplink):
        super().__init__()
        url = tiplink
        self.add_item(discord.ui.Button(emoji='<:paypal:1001287990464749619>', label='Tip', url=url))

class ReviewSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='⭐', label='1', style=discord.ButtonStyle.grey, custom_id='review:1')
    async def onestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('1 star', ephemeral=True)

    @discord.ui.button(emoji='⭐', label='2', style=discord.ButtonStyle.grey, custom_id='review:2')
    async def twostar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('2 star', ephemeral=True)

    @discord.ui.button(emoji='⭐', label='3', style=discord.ButtonStyle.grey, custom_id='review:3')
    async def threestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('3 star', ephemeral=True)

    @discord.ui.button(emoji='⭐', label='4', style=discord.ButtonStyle.grey, custom_id='review:4')
    async def fourstar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('4 star', ephemeral=True)

    @discord.ui.button(emoji='⭐', label='5', style=discord.ButtonStyle.grey, custom_id='review:5')
    async def fivestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('5 star', ephemeral=True)

class CommissionCompleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ReviewSystem())

async def setup(bot):
    await bot.add_cog(CommissionCompleteCog(bot), guilds=[discord.Object(id=guild_id)])