import discord
import aiosqlite
import datetime as DT
import pytz
import yaml
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from typing import Literal

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

freelancer_role_id = data["Roles"]["FREELANCER_ROLE_ID"]
illustrator_role_id = data["Freelancer_Roles"]["ILLUSTRATOR_ROLE_ID"]
vector_artist_role_id = data["Freelancer_Roles"]["VECTOR_ARTIST_ROLE_ID"]
gfx_designer_role_id = data["Freelancer_Roles"]["GFX_DESIGNER_ROLE_ID"]
skin_designer_role_id = data["Freelancer_Roles"]["SKIN_DESIGNER_ROLE_ID"]
render_artist_role_id = data["Freelancer_Roles"]["RENDER_ARTIST_ROLE_ID"]
texture_artist_role_id = data["Freelancer_Roles"]["TEXTURE_ARTIST_ROLE_ID"]
model_designer_role_id = data["Freelancer_Roles"]["MODEL_DESIGNER_ROLE_ID"]
app_developer_role_id = data["Freelancer_Roles"]["APP_DEVELOPER_ROLE_ID"]
bot_developer_role_id = data["Freelancer_Roles"]["BOT_DEVELOPER_ROLE_ID"]
datapack_developer_role_id = data["Freelancer_Roles"]["DATAPACK_DEVELOPER_ROLE_ID"]
plugin_developer_role_id = data["Freelancer_Roles"]["PLUGIN_DEVELOPER_ROLE_ID"]
mod_developer_role_id = data["Freelancer_Roles"]["MOD_DEVELOPER_ROLE_ID"]
forum_designer_role_id = data["Freelancer_Roles"]["FORUM_DESIGNER_ROLE_ID"]
pterodactyl_designer_role_id = data["Freelancer_Roles"]["PTERODACTYL_DESIGNER_ROLE_ID"]
store_designer_role_id = data["Freelancer_Roles"]["STORE_DESIGNER_ROLE_ID"]
uix_designer_role_id = data["Freelancer_Roles"]["UIX_DESIGNER_ROLE_ID"]
web_designer_role_id = data["Freelancer_Roles"]["WEB_DESIGNER_ROLE_ID"]
web_developer_role_id = data["Freelancer_Roles"]["WEB_DEVELOPER_ROLE_ID"]
wix_designer_role_id = data["Freelancer_Roles"]["WIX_DESIGNER_ROLE_ID"]
configurator_role_id = data["Freelancer_Roles"]["CONFIGURATOR_ROLE_ID"]
discord_setup_role_id = data["Freelancer_Roles"]["DISCORD_SETUP_ROLE_ID"]
forum_setup_role_id = data["Freelancer_Roles"]["FORUM_SETUP_ROLE_ID"]
server_setup_role_id = data["Freelancer_Roles"]["SERVER_SETUP_ROLE_ID"]
store_setup_role_id = data["Freelancer_Roles"]["STORE_SETUP_ROLE_ID"]
system_administrator_role_id = data["Freelancer_Roles"]["SYSTEM_ADMINISTRATOR_ROLE_ID"]
animator_role_id = data["Freelancer_Roles"]["ANIMATOR_ROLE_ID"]
content_creator_role_id = data["Freelancer_Roles"]["CONTENT_CREATOR_ROLE_ID"]
intro_creator_role_id = data["Freelancer_Roles"]["INTRO_CREATOR_ROLE_ID"]
motion_designer_role_id = data["Freelancer_Roles"]["MOTION_DESIGNER_ROLE_ID"]
trailer_creator_role_id = data["Freelancer_Roles"]["TRAILER_CREATOR_ROLE_ID"]
video_editor_role_id = data["Freelancer_Roles"]["VIDEO_EDITOR_ROLE_ID"]
writer_role_id = data["Freelancer_Roles"]["WRITER_ROLE_ID"]
builder_role_id = data["Freelancer_Roles"]["BUILDER_ROLE_ID"]
terraformer_role_id = data["Freelancer_Roles"]["TERRAFORMER_ROLE_ID"]
organic_builder_role_id = data["Freelancer_Roles"]["ORGANIC_BUILDER_ROLE_ID"]

class AdminCog(commands.GroupCog, name="admin"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_view(ClaimCommissionTicket())
        self.bot.add_view(TicketSystem())
        self.bot.add_view(TicketClose())
        self.bot.add_view(FreelancerSystem())
        self.bot.add_view(AnswerQuestions())
        self.bot.add_view(Quotes())
        super().__init__()

    @app_commands.command(name="ticketpanel", description="Sends the ticket panel!")
    @app_commands.default_permissions(administrator=True)
    async def ticketpanel(self, interaction: discord.Interaction) -> None:
        view = TicketSystem()
        await interaction.response.send_message("Sent the ticket panel!", ephemeral=True)
        await interaction.channel.send('https://imgur.com/nIKPYG7', view=view)

    @app_commands.command(name="wallet", description="Views the wallet of another member!")
    @app_commands.describe(member="Who's wallet would you like to view?")
    @app_commands.default_permissions(administrator=True)
    async def wallet(self, interaction: discord.Interaction, member: discord.Member) -> None:
        db = await aiosqlite.connect('database.db')
        if member == self.bot.user:
            cursor = await db.execute('SELECT * from funds WHERE member_id=?', (398280171578458122, ))
            a = await cursor.fetchone()
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Total Earnings", value=f"**${a[1]:.2f}**", inline=True)
            embed.add_field(name="Total Spendings", value=f"**${a[2]:.2f}**", inline=True)
            embed.set_author(name=f"{interaction.guild.name}'s Funds", icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (member.id, ))
            a = await cursor.fetchone()
            cursor2 = await db.execute('SELECT * from funds WHERE member_id=?', (member.id, ))
            b = await cursor2.fetchone()
            if a is None:
                embed = discord.Embed(description="This user does not have any information to show!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if b is None:
                    embed = discord.Embed(color=discord.Color.from_str(embed_color))
                    embed.add_field(name="Wallet", value=f"**${a[1]:.2f}**", inline=True)
                    embed.set_author(name=f"{member.name}'s Balance", icon_url=member.avatar.url)
                else:
                    embed.add_field(name="Earnings", value=f"**${b[1]:.2f}**", inline=True)
                    embed.add_field(name="Spendings", value=f"**${b[2]:.2f}**", inline=True)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="resetwallet", description="Resets the earnings of Mixelate!")
    @app_commands.default_permissions(administrator=True)
    async def resetwallet(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        await db.execute('UPDATE funds SET earnings=? WHERE member_id=?', (0, 398280171578458122))
        await db.commit()
        await db.close()
        embed = discord.Embed(description="Mixelate's walet has been reset!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="strip", description="Strips the all of the member's freelancer roles!")
    @app_commands.describe(member="Who would you like to strip?")
    @app_commands.default_permissions(administrator=True)
    async def strip(self, interaction: discord.Interaction, member: discord.Member) -> None:
        embed = discord.Embed(description="Stripping...", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)
        roles = [
            freelancer_role_id, illustrator_role_id, vector_artist_role_id, gfx_designer_role_id,
            skin_designer_role_id, render_artist_role_id, texture_artist_role_id, model_designer_role_id,
            app_developer_role_id, bot_developer_role_id, datapack_developer_role_id, plugin_developer_role_id,
            mod_developer_role_id, forum_designer_role_id, pterodactyl_designer_role_id, store_designer_role_id,
            uix_designer_role_id, web_designer_role_id, web_developer_role_id, wix_designer_role_id,
            configurator_role_id, discord_setup_role_id, forum_setup_role_id, server_setup_role_id,
            store_setup_role_id, system_administrator_role_id, animator_role_id, content_creator_role_id,
            intro_creator_role_id, motion_designer_role_id, trailer_creator_role_id, video_editor_role_id,
            writer_role_id, builder_role_id, terraformer_role_id, organic_builder_role_id
            ]
        for role_id in roles:
            if role := interaction.guild.get_role(role_id):
                await member.remove_roles(role)
        embed = discord.Embed(description=f"Sucessfully stripped all of {member.mention}'s freelancer roles!", color=discord.Color.from_str(embed_color))
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="addrole", description="Adds a role to a member!")
    @app_commands.describe(member="Who would you like to add a role to?")
    @app_commands.describe(category="What type of role category would you like to view?")
    @app_commands.describe(role="What role would you like to give the member?")
    @app_commands.default_permissions(administrator=True)
    async def addrole(self, interaction: discord.Interaction, member: discord.Member, category: Literal["Design", "Development", "Web", "Setups", "Video", "Creative"], role: str) -> None:
        if role == "Illustrator":
            role_id = illustrator_role_id
        if role == "Vector Artist":
            role_id = vector_artist_role_id
        if role == "GFX Designer":
            role_id = gfx_designer_role_id
        if role == "Skin Designer":
            role_id = skin_designer_role_id
        if role == "Render Artist":
            role_id = render_artist_role_id
        if role == "Texture Artist":
            role_id = texture_artist_role_id
        if role == "Model Designer":
            role_id = model_designer_role_id
        if role == "App Developer":
            role_id = app_developer_role_id
        if role == "Bot Developer":
            role_id = bot_developer_role_id
        if role == "Datapack Developer":
            role_id = datapack_developer_role_id
        if role == "Plugin Developer":
            role_id = plugin_developer_role_id
        if role == "Mod Developer":
            role_id = mod_developer_role_id
        if role == "Forum Designer":
            role_id = forum_designer_role_id
        if role == "Pterodactyl Designer":
            role_id = pterodactyl_designer_role_id
        if role == "Store Designer":
            role_id = store_designer_role_id
        if role == "UIX Designer":
            role_id = uix_designer_role_id
        if role == "Web Designer":
            role_id = web_designer_role_id
        if role == "Web Developer":
            role_id = web_developer_role_id
        if role == "WIX Designer":
            role_id = wix_designer_role_id
        if role == "Configurator":
            role_id = configurator_role_id
        if role == "Discord Setup":
            role_id = discord_setup_role_id
        if role == "Forum Setup":
            role_id = forum_setup_role_id
        if role == "Server Setup":
            role_id = server_setup_role_id
        if role == "Store Setup":
            role_id = store_setup_role_id
        if role == "System Administrator":
            role_id = system_administrator_role_id
        if role == "Animator":
            role_id = animator_role_id
        if role == "Content Creator":
            role_id = content_creator_role_id
        if role == "Intro Creator":
            role_id = intro_creator_role_id
        if role == "Motion Designer":
            role_id = motion_designer_role_id
        if role == "Trailer Creator":
            role_id = trailer_creator_role_id
        if role == "Video Editor":
            role_id = video_editor_role_id
        if role == "Writer":
            role_id = writer_role_id
        if role == "Builder":
            role_id = builder_role_id
        if role == "Terraformer":
            role_id = terraformer_role_id
        if role == "Organic Builder":
            role_id = organic_builder_role_id
        role = interaction.guild.get_role(role_id)
        if role in member.roles:
            embed = discord.Embed(description=f"{member.mention} already has {role.mention}!", color=discord.Color.red())
        else:
            try:
                await member.add_roles(role)
                embed = discord.Embed(description=f"{member.mention} was successfully given the {role.mention} role!", color=discord.Color.from_str(embed_color))
            except discord.Forbidden:
                embed = discord.Embed(description=f"I cannot add {role.mention} to {member.mention} because my role is not above {role.mention}!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @addrole.autocomplete('role')
    async def autocomplete_callback(self, interaction: discord.Interaction, curent: str):
        if interaction.namespace.category == 'Design':
            return [
                app_commands.Choice(name='Illustrator', value='Illustrator'),
                app_commands.Choice(name='Vector Artist', value='Vector Artist'),
                app_commands.Choice(name='GFX Designer', value='GFX Designer'),
                app_commands.Choice(name='Skin Designer', value='Skin Designer'),
                app_commands.Choice(name='Render Artist', value='Render Artist'),
                app_commands.Choice(name='Texture Artist', value='Texture Artist'),
                app_commands.Choice(name='Model Designer', value='Model Designer')
            ]
        if interaction.namespace.category == 'Development':
            return [
                app_commands.Choice(name='App Developer', value='App Developer'),
                app_commands.Choice(name='Bot Developer', value='Bot Developer'),
                app_commands.Choice(name='Datapack Developer', value='Datapack Developer'),
                app_commands.Choice(name='Plugin Developer', value='Plugin Developer'),
                app_commands.Choice(name='Mod Developer', value='Mod Developer')
            ]
        if interaction.namespace.category == 'Web':
            return [
                app_commands.Choice(name='Forum Designer', value='Forum Designer'),
                app_commands.Choice(name='Pterodactyl Designer', value='Pterodactyl Designer'),
                app_commands.Choice(name='Store Designer', value='Store Designer'),
                app_commands.Choice(name='UIX Designer', value='UIX Designer'),
                app_commands.Choice(name='Web Designer', value='Web Designer'),
                app_commands.Choice(name='Web Developer', value='Web Developer'),
                app_commands.Choice(name='WIX Designer', value='WIX Designer')
            ]
        if interaction.namespace.category == 'Setups':
            return [
                app_commands.Choice(name='Configurator', value='Configurator'),
                app_commands.Choice(name='Discord Setup', value='Discord Setup'),
                app_commands.Choice(name='Forum Setup', value='Forum Setup'),
                app_commands.Choice(name='Server Setup', value='Server Setup'),
                app_commands.Choice(name='Store Setup', value='Store Setup'),
                app_commands.Choice(name='System Administrator', value='System Administrator')
            ]
        if interaction.namespace.category == 'Video':
            return [
                app_commands.Choice(name='Animator', value='Animator'),
                app_commands.Choice(name='Content Creator', value='Content Creator'),
                app_commands.Choice(name='Intro Creator', value='Intro Creator'),
                app_commands.Choice(name='Motion Designer', value='Motion Designer'),
                app_commands.Choice(name='Trailer Creator', value='Trailer Creator'),
                app_commands.Choice(name='Video Editor', value='Video Editor')
            ]
        if interaction.namespace.category == 'Creative':
            return [
                app_commands.Choice(name='Builder', value='Builder'),
                app_commands.Choice(name='Terraformer', value='Terraformer'),
                app_commands.Choice(name='Organic Builder', value='Organic Builder')
            ]

    @app_commands.command(name="removerole", description="Removes a role from a member!")
    @app_commands.describe(member="Who would you like to remove a role from?")
    @app_commands.describe(category="What type of role category would you like to view?")
    @app_commands.describe(role="What role would you like to remove from the member?")
    @app_commands.default_permissions(administrator=True)
    async def removerole(self, interaction: discord.Interaction, member: discord.Member, category: Literal["Design", "Development", "Web", "Setups", "Video", "Creative"], role: str) -> None:
        if role == "Illustrator":
            role_id = illustrator_role_id
        if role == "Vector Artist":
            role_id = vector_artist_role_id
        if role == "GFX Designer":
            role_id = gfx_designer_role_id
        if role == "Skin Designer":
            role_id = skin_designer_role_id
        if role == "Render Artist":
            role_id = render_artist_role_id
        if role == "Texture Artist":
            role_id = texture_artist_role_id
        if role == "Model Designer":
            role_id = model_designer_role_id
        if role == "App Developer":
            role_id = app_developer_role_id
        if role == "Bot Developer":
            role_id = bot_developer_role_id
        if role == "Datapack Developer":
            role_id = datapack_developer_role_id
        if role == "Plugin Developer":
            role_id = plugin_developer_role_id
        if role == "Mod Developer":
            role_id = mod_developer_role_id
        if role == "Forum Designer":
            role_id = forum_designer_role_id
        if role == "Pterodactyl Designer":
            role_id = pterodactyl_designer_role_id
        if role == "Store Designer":
            role_id = store_designer_role_id
        if role == "UIX Designer":
            role_id = uix_designer_role_id
        if role == "Web Designer":
            role_id = web_designer_role_id
        if role == "Web Developer":
            role_id = web_developer_role_id
        if role == "WIX Designer":
            role_id = wix_designer_role_id
        if role == "Configurator":
            role_id = configurator_role_id
        if role == "Discord Setup":
            role_id = discord_setup_role_id
        if role == "Forum Setup":
            role_id = forum_setup_role_id
        if role == "Server Setup":
            role_id = server_setup_role_id
        if role == "Store Setup":
            role_id = store_setup_role_id
        if role == "System Administrator":
            role_id = system_administrator_role_id
        if role == "Animator":
            role_id = animator_role_id
        if role == "Content Creator":
            role_id = content_creator_role_id
        if role == "Intro Creator":
            role_id = intro_creator_role_id
        if role == "Motion Designer":
            role_id = motion_designer_role_id
        if role == "Trailer Creator":
            role_id = trailer_creator_role_id
        if role == "Video Editor":
            role_id = video_editor_role_id
        if role == "Writer":
            role_id = writer_role_id
        if role == "Builder":
            role_id = builder_role_id
        if role == "Terraformer":
            role_id = terraformer_role_id
        if role == "Organic Builder":
            role_id = organic_builder_role_id
        role = interaction.guild.get_role(role_id)
        if role not in member.roles:
            embed = discord.Embed(description=f"{member.mention} does not have the {role.mention} role!", color=discord.Color.red())
        else:
            try:
                await member.remove_roles(role)
                embed = discord.Embed(description=f"{member.mention} was successfully removed from the {role.mention} role!", color=discord.Color.from_str(embed_color))
            except discord.Forbidden:
                embed = discord.Embed(description=f"I cannot remove {role.mention} from {member.mention} because my role is not above {role.mention}!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @removerole.autocomplete('role')
    async def autocomplete_callback(self, interaction: discord.Interaction, curent: str):
        if interaction.namespace.category == 'Design':
            return [
                app_commands.Choice(name='Illustrator', value='Illustrator'),
                app_commands.Choice(name='Vector Artist', value='Vector Artist'),
                app_commands.Choice(name='GFX Designer', value='GFX Designer'),
                app_commands.Choice(name='Skin Designer', value='Skin Designer'),
                app_commands.Choice(name='Render Artist', value='Render Artist'),
                app_commands.Choice(name='Texture Artist', value='Texture Artist'),
                app_commands.Choice(name='Model Designer', value='Model Designer')
            ]
        if interaction.namespace.category == 'Development':
            return [
                app_commands.Choice(name='App Developer', value='App Developer'),
                app_commands.Choice(name='Bot Developer', value='Bot Developer'),
                app_commands.Choice(name='Datapack Developer', value='Datapack Developer'),
                app_commands.Choice(name='Plugin Developer', value='Plugin Developer'),
                app_commands.Choice(name='Mod Developer', value='Mod Developer')
            ]
        if interaction.namespace.category == 'Web':
            return [
                app_commands.Choice(name='Forum Designer', value='Forum Designer'),
                app_commands.Choice(name='Pterodactyl Designer', value='Pterodactyl Designer'),
                app_commands.Choice(name='Store Designer', value='Store Designer'),
                app_commands.Choice(name='UIX Designer', value='UIX Designer'),
                app_commands.Choice(name='Web Designer', value='Web Designer'),
                app_commands.Choice(name='Web Developer', value='Web Developer'),
                app_commands.Choice(name='WIX Designer', value='WIX Designer')
            ]
        if interaction.namespace.category == 'Setups':
            return [
                app_commands.Choice(name='Configurator', value='Configurator'),
                app_commands.Choice(name='Discord Setup', value='Discord Setup'),
                app_commands.Choice(name='Forum Setup', value='Forum Setup'),
                app_commands.Choice(name='Server Setup', value='Server Setup'),
                app_commands.Choice(name='Store Setup', value='Store Setup'),
                app_commands.Choice(name='System Administrator', value='System Administrator')
            ]
        if interaction.namespace.category == 'Video':
            return [
                app_commands.Choice(name='Animator', value='Animator'),
                app_commands.Choice(name='Content Creator', value='Content Creator'),
                app_commands.Choice(name='Intro Creator', value='Intro Creator'),
                app_commands.Choice(name='Motion Designer', value='Motion Designer'),
                app_commands.Choice(name='Trailer Creator', value='Trailer Creator'),
                app_commands.Choice(name='Video Editor', value='Video Editor')
            ]
        if interaction.namespace.category == 'Creative':
            return [
                app_commands.Choice(name='Builder', value='Builder'),
                app_commands.Choice(name='Terraformer', value='Terraformer'),
                app_commands.Choice(name='Organic Builder', value='Organic Builder')
            ]

    @app_commands.command(name="warn", description="Warns a member!")
    @app_commands.describe(member="Who would you like to warn?")
    @app_commands.describe(reason="What is the reason to your warn?")
    @app_commands.default_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM warns')
        rows = await cursor.fetchall()
        time = datetime.now(tz=pytz.timezone('America/Tijuana'))
        formatted = time.strftime("%m/%d/%y, %I:%M %p")
        b = DT.datetime.now().timestamp()
        b = int(b)
        try:
            await db.execute('INSERT INTO warns VALUES (?,?,?,?,?);', (member.id, f'{interaction.user}', f'{reason}', f'{formatted}', len(rows)))
            embed = discord.Embed(description=f"You were warned in {interaction.guild.name} for: \n\n**{reason}**", color=discord.Color.from_str(embed_color))
            await member.send(embed=embed)
            embed = discord.Embed(description=f"You sucessfully warned {interaction.user.mention} for **{reason}**!", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            embed = discord.Embed(description=f"Failed to send {member.mention} a warning DM!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="warns", description="Views the warns of a member!")
    @app_commands.describe(member="Who's warnings would you like to view?")
    @app_commands.default_permissions(administrator=True)
    async def warns(self, interaction: discord.Interaction, member: discord.Member) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM warns WHERE member_id=?', (member.id,))
        rows = await cursor.fetchall()
        await db.close()
        member = interaction.guild.get_member(member.id)
        embed = discord.Embed(
            title=f"Warns of {member}",
            color=discord.Color.from_str(embed_color))
        if rows == []:
            embed.add_field(name="Clean History", value=f"{member.mention} has a clean history!")
        else:
            for row in rows:
                embed.add_field(name=f"Case #{row[4]}", value=f"Reason: **{row[2]}** \nIssuer: **{row[1]}** \nTime Issued: **{row[3]}** \n")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCog(bot), guilds=[discord.Object(id=guild_id)])