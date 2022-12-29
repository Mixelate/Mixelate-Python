import discord
import yaml
from discord.ext import commands

from modals.order import Order

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class OrderDesignDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Illustrator'),
            discord.SelectOption(label='Model Designer'),
            discord.SelectOption(label='Texture Artist'),
            discord.SelectOption(label='Render Artist'),
            discord.SelectOption(label='Skin Designer'),
            discord.SelectOption(label='GFX Designer'),
            discord.SelectOption(label='Vector Artist'),
        ]

        super().__init__(placeholder="Select an option!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        await interaction.response.send_modal(Order(category))

class OrderDesignDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(OrderDesignDropdown())

class OrderDesignCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(OrderDesignCog(bot), guilds=[discord.Object(id=guild_id)])