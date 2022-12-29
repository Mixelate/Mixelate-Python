import discord
import aiosqlite
import yaml
from discord.ext import commands

from modals.quote import Quote
from modals.question import Question

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class FreelancerSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='💰', label='Quote', style=discord.ButtonStyle.green, custom_id='freelancer:1')
    async def quote(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE freelancer_message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        role = interaction.guild.get_role(a[1])
        if role in interaction.user.roles:
            await interaction.response.send_modal(Quote())
        else:
            await interaction.response.send_message("You are not allowed to send a quote for this type of commission!", ephemeral=True)

    @discord.ui.button(emoji='❔', label='Question', style=discord.ButtonStyle.grey, custom_id='freelancer:2')
    async def question(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE freelancer_message_id=?', (interaction.message.id, ))
        a = await cursor.fetchone()
        role = interaction.guild.get_role(a[1])
        if role in interaction.user.roles:
            await interaction.response.send_modal(Question())
        else:
            await interaction.response.send_message("You are not allowed to ask questions for this type of commission!", ephemeral=True)

class FreelancerSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(FreelancerSystem())

async def setup(bot):
    await bot.add_cog(FreelancerSystemCog(bot), guilds=[discord.Object(id=guild_id)])