import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class TicketCog(commands.GroupCog, name="ticket"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="leave", description="Leaves the ticket!")
    async def leave(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message("This is not a commission channel!", ephemeral=True)
        else:
            if a[3] == interaction.user.id:
                await interaction.response.send_message("Removing...", ephemeral=True)
                await db.execute('UPDATE commissions SET freelancer_id=? WHERE channel_id=? AND freelancer_id=?', ('null', interaction.channel.id, interaction.user.id))
                await interaction.channel.set_permissions(interaction.user,
                                                send_messages=False,
                                                read_messages=False,
                                                add_reactions=False,
                                                embed_links=False,
                                                read_message_history=False,
                                                external_emojis=False,
                                                use_application_commands=False)
            else:
                await interaction.response.send_message("You are not the freelancer for this commission!", ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="repost", description="Reposts the ticket!")
    async def repost(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="addcharge", description="Creates an additional invoice!")
    async def addcharge(self, interaction: discord.Interaction, amount: int) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="newprice", description="Sets the new price of the commission!")
    async def newprice(self, interaction: discord.Interaction, amount: int) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="begin", description="Starts the commission!")
    async def begin(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="transcript", description="Generates a ticket transcript!")
    async def transcript(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="close", description="Closes the ticket in the specified time!")
    async def close(self, interaction: discord.Interaction, time: str) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="review", description="Review the freelancer!")
    async def review(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="tip", description="Tip the freelancer!")
    async def tip(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

class TicketTicketCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ticket", description="Opens the Ticket GUI!")
    async def ticketticket(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(TicketTicketCog(bot))