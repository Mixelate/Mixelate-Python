import discord
import aiosqlite
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
freelancer_commission_channel_id = data["Tickets"]["FREELANCER_COMMISSION_CHANNEL_ID"]

class Quotes(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='✅', label='Accept', style=discord.ButtonStyle.green, custom_id='quotes:1')
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT freelancer_message_id FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        rows = await cursor.fetchone()
        channel = interaction.guild.get_channel(freelancer_commission_channel_id)
        freelancer_message = channel.get_partial_message(rows[0])
        await freelancer_message.delete()
        await interaction.message.delete()
        cursor = await db.execute('SELECT * FROM quotes WHERE commissions_channel=?', (interaction.channel.id, ))
        rows = await cursor.fetchone()
        freelancer = interaction.client.get_user(rows[1])
        await interaction.channel.set_permissions(freelancer,
            send_messages=True,
            read_messages=True,
            add_reactions=True,
            embed_links=True,
            read_message_history=True,
            external_emojis=True,
            use_application_commands=True)
        await db.execute('UPDATE commissions SET freelancer_message_id=? WHERE channel_id=?', ('null', interaction.channel.id))
        await db.execute('UPDATE commissions SET freelancer_id=? WHERE channel_id=?', (rows[1], interaction.channel.id))
        embed = discord.Embed(title="Accepted Freelancer",
                            description=f"""
Welcome to the commission, **{freelancer.name}**!

Please discuss everything and make sure everything is clear. Once you set everything in place, ask a Staff Member to create an invoice for you.

Be sure to not start any work until the invoice has been confirmed as paid!
""",
                            color=discord.Color.from_str(embed_color))
        await interaction.channel.send(embed=embed, content=f'{freelancer.mention}')
        await db.execute('DELETE FROM quotes WHERE commissions_channel=?', (interaction.channel.id, ))
        await interaction.response.send_message("You've accepted their quote!", ephemeral=True)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='❌', label='Decline', style=discord.ButtonStyle.grey, custom_id='quotes:2')
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        await db.execute('DELETE FROM quotes WHERE commissions_channel=?', (interaction.channel.id, ))
        await interaction.message.delete()
        await interaction.response.send_message("You've declined their quote!", ephemeral=True)
        await db.commit()
        await db.close()

class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(Quotes())

async def setup(bot):
    await bot.add_cog(QuotesCog(bot), guilds=[discord.Object(id=guild_id)])