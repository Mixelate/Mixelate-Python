import discord
import aiosqlite
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
application_reviewer_role_id = data["Roles"]["APPLICATION_REVIEWER_ROLE_ID"]

class ClaimApplicationTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='📫', label='Claim', style=discord.ButtonStyle.grey, custom_id='claim_application:1')
    async def claimapp(self, interaction: discord.Interaction, button: discord.ui.Button):
        application_reviewer = interaction.guild.get_role(application_reviewer_role_id)
        if application_reviewer in interaction.user.roles:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM applications WHERE claim_id=?', (interaction.message.id, ))
            a = await cursor.fetchone()
            channel = interaction.guild.get_channel(a[1])
            
            await channel.set_permissions(interaction.user,
                                             view_channel=True,
                                             send_messages=True,
                                             read_messages=True,
                                             add_reactions=True,
                                             embed_links=True,
                                             read_message_history=True,
                                             external_emojis=True,
                                             use_application_commands=True)
            
            await interaction.response.send_message(f"You've been added to <#{a[1]}>", ephemeral=True)
            embed = discord.Embed(title="Application Reviewer Joined",
                description=f"An application reviewer has joined! **{interaction.user.name}** will be reviewing your application as soon as possible!",
                color=discord.Color.from_str(embed_color))
            await channel.send(content=interaction.user.mention, embed=embed)
            await db.execute('UPDATE applications SET application_reviewer=? WHERE claim_id=?', (interaction.user.id, interaction.message.id))
            await db.execute('UPDATE applications SET claim_id=? WHERE claim_id=?', ('null', interaction.message.id))
            await db.commit()
            await db.close()
            await interaction.message.delete()
        else:
            await interaction.response.send_message("You are not allowed to claim these types of tickets!", ephemeral=True)

class ClaimApplicationTicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ClaimApplicationTicket())

async def setup(bot):
    await bot.add_cog(ClaimApplicationTicketCog(bot), guilds=[discord.Object(id=guild_id)])