import discord
import yaml
from discord.ext import commands

from dropdowns.order.orderdesign import OrderDesignDropdownView
from dropdowns.order.orderdevelopment import OrderDevelopmentDropdownView
from dropdowns.order.orderweb import OrderWebDropdownView
from dropdowns.order.ordersetups import OrderSetupsDropdownView
from dropdowns.order.ordervideo import OrderVideoDropdownView
from dropdowns.order.ordercreative import OrderCreativeDropdownView

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class OrderDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Design'),
            discord.SelectOption(label='Development'),
            discord.SelectOption(label='Web'),
            discord.SelectOption(label='Setups'),
            discord.SelectOption(label='Video'),
            discord.SelectOption(label='Creative'),
        ]

        super().__init__(placeholder="Select an option!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        embed=discord.Embed(
        description="Choose a commission type below!", 
        color=discord.Color.from_str(embed_color))
        if self.values[0] == "Design":
            await interaction.response.edit_message(content=None, embed=embed, view=OrderDesignDropdownView())
        if self.values[0] == "Development":
            await interaction.response.edit_message(content=None, embed=embed, view=OrderDevelopmentDropdownView())
        if self.values[0] == "Web":
            await interaction.response.edit_message(content=None, embed=embed, view=OrderWebDropdownView())
        if self.values[0] == "Setups":
            await interaction.response.edit_message(content=None, embed=embed, view=OrderSetupsDropdownView())
        if self.values[0] == "Video":
            await interaction.response.edit_message(content=None, embed=embed, view=OrderVideoDropdownView())
        if self.values[0] == "Creative":
            await interaction.response.edit_message(content=None, embed=embed, view=OrderCreativeDropdownView())

class OrderDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(OrderDropdown())

class OrderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(OrderCog(bot), guilds=[discord.Object(id=guild_id)])