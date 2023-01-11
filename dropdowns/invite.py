import discord
import yaml
from discord.ext import commands

from discord import ui, Interaction
from discord.ui import UserSelect

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class InviteDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @ui.select(cls=UserSelect, placeholder="Select a member to invite!")
    async def my_user_select(self, interaction: Interaction, select: UserSelect):

        user = [
            (f"{user.name}", user.id)
            for user in select.values
        ]
        member = interaction.guild.get_member(user[0][1])
        await interaction.channel.set_permissions(member,
            send_messages=True,
            read_messages=True,
            add_reactions=True,
            embed_links=True,
            read_message_history=True,
            external_emojis=True,
            use_application_commands=True)
        embed = discord.Embed(description=f"{member.mention} was invited to the ticket by {interaction.user.mention}!", color=discord.Color.from_str(embed_color))
        await interaction.channel.send(content=member.mention, embed=embed)
        embed = discord.Embed(description=f"Sucessfully invited {member.mention} to the ticket!", color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed, view=None)

class InviteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(InviteCog(bot), guilds=[discord.Object(id=guild_id)])