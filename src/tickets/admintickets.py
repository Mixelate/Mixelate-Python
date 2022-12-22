import discord
import yaml
from discord import app_commands, ui
from discord.ext import commands

from buttons.commissions.claimcommissionticket import ClaimCommissionTicket
from buttons.tickets.ticketclose import TicketClose
from buttons.tickets.ticketsystem import TicketSystem
from buttons.freelancer.freelancersystem import FreelancerSystem
from buttons.questions.answerquestions import AnswerQuestions
from buttons.quotes.quotes import Quotes


with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ClaimCommissionTicket())
        self.bot.add_view(TicketSystem())
        self.bot.add_view(TicketClose())
        self.bot.add_view(FreelancerSystem())
        self.bot.add_view(AnswerQuestions())
        self.bot.add_view(Quotes())

    @app_commands.command(name="panel", description="Sends the ticket panel!")
    @app_commands.guilds(discord.Object(id=guild_id))
    @app_commands.default_permissions(administrator=True)
    async def panel(self, interaction: discord.Interaction):
        view = TicketSystem()
        await interaction.response.send_message("Sent the ticket panel!", ephemeral=True)
        await interaction.channel.send('https://imgur.com/nIKPYG7', view=view)

async def setup(bot):
    await bot.add_cog(TicketsCog(bot), guilds=[discord.Object(id=guild_id)])