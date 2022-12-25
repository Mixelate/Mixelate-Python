import discord
import aiosqlite
import yaml

from buttons.tickets.ticketclose import TicketClose

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
support_ticket_category_id = data["Tickets"]["SUPPORT_TICKET_CATEGORY_ID"]
support_specialist_role_id = data["Roles"]["SUPPORT_SPECIALIST_ROLE_ID"]

class Support(discord.ui.Modal, title='Support Ticket'):

    description = discord.ui.TextInput(
        label='What do you need help with?',
        style=discord.TextStyle.long,
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('The ticket is being created...', ephemeral=True)
        
        db = await aiosqlite.connect('database.db')

        category_channel = interaction.guild.get_channel(support_ticket_category_id)
        ticket_channel = await category_channel.create_text_channel(
            f"support-{interaction.user.name}")
        await ticket_channel.set_permissions(interaction.guild.get_role(interaction.guild.id),
                                         send_messages=False,
                                         read_messages=False)

        cursor = await db.execute('SELECT valid_roles FROM tickets')
        rows = await cursor.fetchall()
        for (role_id,) in rows:

            role = interaction.guild.get_role(role_id)
            
            await ticket_channel.set_permissions(role,
                                             send_messages=True,
                                             read_messages=True,
                                             add_reactions=True,
                                             embed_links=True,
                                             read_message_history=True,
                                             external_emojis=True)
        
        await ticket_channel.set_permissions(interaction.user,
                                         send_messages=True,
                                         read_messages=True,
                                         add_reactions=True,
                                         embed_links=True,
                                         attach_files=True,
                                         read_message_history=True,
                                         external_emojis=True)

        await db.close()

        await interaction.edit_original_response(content=f'The ticket has been created at {ticket_channel.mention}.')

        support_specialist = interaction.guild.get_role(support_specialist_role_id)

        await ticket_channel.send(content=f'{support_specialist.mention}', delete_after=1)

        x = f'{interaction.user.mention}'

        view = TicketClose()
      
        embed=discord.Embed(title="", 
        description=f"""
A member of our team will be with you shortly. You'll be notified when you receive a response!

**__Details__**: ```
{self.description.value}
```
""", 
        color=discord.Color.from_str(embed_color))

        await ticket_channel.send(content=x, embed=embed, view=view)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)