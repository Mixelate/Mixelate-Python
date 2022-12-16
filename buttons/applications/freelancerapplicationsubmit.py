import discord
import aiosqlite
import datetime as DT
import yaml
from discord.ext import commands

from buttons.applications.claimapplicationticket import ClaimApplicationTicket
from buttons.tickets.ticketclose import TicketClose

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
application_ticket_category_id = data["Tickets"]["APPLICATION_TICKET_CATEGORY_ID"]
staff_claim_ticket_channel_id = data["Tickets"]["STAFF_CLAIM_TICKET_CHANNEL_ID"]
application_reviewer_role_id = data["Roles"]["APPLICATION_REVIEWER_ROLE_ID"]

class FreelancerApplicationSubmit(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Submit', emoji='✅', style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        if self.view.stored_roles == None:
            await interaction.response.send_message("You must select at least one role before submitting!", ephemeral=True)
        else:
            await interaction.response.edit_message(content='The ticket is being created...', embed=None, view=None)

            db = await aiosqlite.connect('database.db')


            category_channel = interaction.guild.get_channel(application_ticket_category_id)
            ticket_channel = await category_channel.create_text_channel(
                f"apply-{interaction.user.name}")
            await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                            send_messages=False,
                                            read_messages=False)
            
            await ticket_channel.set_permissions(interaction.user,
                                            send_messages=True,
                                            read_messages=True,
                                            add_reactions=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True,
                                            use_application_commands=True)
            
            claim_channel = interaction.guild.get_channel(staff_claim_ticket_channel_id)
            application_reviewer = interaction.guild.get_role(application_reviewer_role_id)

            a = DT.datetime.now().timestamp()
            b = int(a)

            embed=discord.Embed( 
            description=f"""
**Freelancer Application <t:{b}:R>**
```
{self.view.roles}
```
""",
            color=discord.Color.from_str(embed_color))

            view = ClaimApplicationTicket()

            a = await claim_channel.send(content=application_reviewer.mention, embed=embed, view=view)

            await db.execute('INSERT INTO applications VALUES (?,?,?,?,?);', (interaction.user.id, ticket_channel.id, self.view.stored_roles, a.id, 'null'))

            await db.commit()
            await db.close()

            await interaction.edit_original_response(content=f'The ticket has been created at {ticket_channel.mention}.')

            x = f'{interaction.user.mention}'

            view = TicketClose()

            embed=discord.Embed(title="", 
            description=f"""
**__Position__**:
Freelancer

**__Roles__**:
{self.view.roles}

*Note: Be sure to post your portfolio below so you have a bigger chance of being accepted!*
""", 
            color=discord.Color.from_str(embed_color))

            await ticket_channel.send(content=x, embed=embed, view=view)

class FreelancerApplicationSubmitCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(FreelancerApplicationSubmitCog(bot), guilds=[discord.Object(id=guild_id)])