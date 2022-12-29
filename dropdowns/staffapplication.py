import discord
import yaml
import aiosqlite
import datetime as DT
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

class StaffApplicationDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='-------Commissions-------'),
            discord.SelectOption(label='Commission Manager'),
            discord.SelectOption(label='-------Applications-------'),
            discord.SelectOption(label='Application Reviewer'),
            discord.SelectOption(label='-------Support-------'),
            discord.SelectOption(label='Support Specialist'),
        ]

        super().__init__(placeholder="Choose the role that you're applying for!", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        badroles = ["-------Commissions-------", "-------Applications-------", "-------Support-------"]
        if self.values[0] in badroles:
            embed = discord.Embed(description=f"You may not choose `{self.values[0]}`! Please make sure it's not a category header.", color=discord.Color.red())
            await interaction.response.edit_message(content=None, embed=embed, view=None)
            return
        stored_roles = (', '.join(self.values))
        roles = (' \n'.join(self.values))

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
**Staff Application <t:{b}:R>**
```
{roles}
```
""",
        color=discord.Color.from_str(embed_color))

        view = ClaimApplicationTicket()

        a = await claim_channel.send(content=application_reviewer.mention, embed=embed, view=view)

        await db.execute('INSERT INTO applications VALUES (?,?,?,?,?);', (interaction.user.id, ticket_channel.id, stored_roles, a.id, 'null'))

        await db.commit()
        await db.close()

        await interaction.edit_original_response(content=f'The ticket has been created at {ticket_channel.mention}.')

        x = f'{interaction.user.mention}'

        view = TicketClose()

        embed=discord.Embed(title="", 
        description=f"""
**__Position__**:
Staff

**__Roles__**:
{roles}

*Note: Be sure to post your portfolio below so you have a bigger chance of being accepted!*
""", 
        color=discord.Color.from_str(embed_color))

        await ticket_channel.send(content=x, embed=embed, view=view)

class StaffApplicationDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(StaffApplicationDropdown())

class StaffApplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(StaffApplicationCog(bot), guilds=[discord.Object(id=guild_id)])