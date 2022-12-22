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

    @app_commands.command(name="add", description="Adds someone to the ticket!")
    @app_commands.describe(user="Who would you like to add to the ticket?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def add(self, interaction: discord.Interaction, user: discord.Member) -> None:
        valid_names = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_names):
            await interaction.channel.set_permissions(user,
                                                send_messages=True,
                                                read_messages=True,
                                                add_reactions=True,
                                                embed_links=True,
                                                read_message_history=True,
                                                external_emojis=True)

            await interaction.response.send_message('Added.')
        else:
            await interaction.response.send_message('This is not a valid ticket!', ephemeral=True)

    @app_commands.command(name="remove", description="Removes someone from the ticket!")
    @app_commands.describe(user="Who would you like to remove from the ticket?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def remove(self, interaction: discord.Interaction, user: discord.Member) -> None:
        valid_names = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_names):
            await interaction.channel.set_permissions(user,
                                                send_messages=False,
                                                read_messages=False,
                                                add_reactions=False,
                                                embed_links=False,
                                                read_message_history=False,
                                                external_emojis=False,
                                                use_application_commands=False)
            await interaction.response.send_message('Removed.')
        else:
            await interaction.response.send_message('This is not a valid ticket!', ephemeral=True)

    @app_commands.command(name="close", description="Closes the ticket.")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def close(self, interaction: discord.Interaction):
        valid_names = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_names):
            view = TicketClose()
            embed = discord.Embed(
                title="Closure Confirmation",
                description=
                "Click the button if you want to close the ticket.",
                color=0x00a8ff)
            await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(TicketsCog(bot), guilds=[discord.Object(id=guild_id)])