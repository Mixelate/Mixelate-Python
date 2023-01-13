import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
accepted_application_payment = data["General"]["ACCEPTED_APPLICATION_PAYMENT"]
declined_application_payment = data["General"]["DECLINED_APPLICATION_PAYMENT"]
freelancer_dashboard_command = data["Commands"]["FREELANCER_DASHBOARD_COMMAND"]

commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]
application_reviewer_role_id = data["Roles"]["APPLICATION_REVIEWER_ROLE_ID"]
support_specialist_role_id = data["Roles"]["SUPPORT_SPECIALIST_ROLE_ID"]
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

claim_ticket_channel_id = data["Tickets"]["STAFF_CLAIM_TICKET_CHANNEL_ID"]
freelancer_commission_channel_id = data["Tickets"]["FREELANCER_COMMISSION_CHANNEL_ID"]
freelancer_announcement_channel_id = data["Tickets"]["FREELANCER_ANNOUNCEMENT_CHANNEL_ID"]


class ApplicationManagerDropdown(discord.ui.Select):
    def __init__(self, roles):
        self.roles = roles

        options = [discord.SelectOption(label=x) for x in roles]

        super().__init__(placeholder="Choose all the you wish to give them!", min_values=1, max_values=len(roles), options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Accepting...", view=None, embed=None)
        e = await interaction.original_response()
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        ids = []
        try:
            channel = interaction.guild.get_channel(claim_ticket_channel_id)
            claim_message = channel.get_partial_message(a[3])
            await claim_message.delete()
        except:
            pass
        for roles in self.values:
            if roles == "Commission Manager":
                id = commission_manager_role_id
                ids.append(id)
            if roles == "Application Reviewer":
                id = application_reviewer_role_id
                ids.append(id)
            if roles == "Support Specialist":
                id = support_specialist_role_id
                ids.append(id)
            if roles == "Illustrator":
                id = illustrator_role_id
                ids.append(id)
            if roles == "Vector Artist":
                id = vector_artist_role_id
                ids.append(id)
            if roles == "GFX Designer":
                id = gfx_designer_role_id
                ids.append(id)
            if roles == "Skin Designer":
                id = skin_designer_role_id
                ids.append(id)
            if roles == "Render Artist":
                id = render_artist_role_id
                ids.append(id)
            if roles == "Texture Arist":
                id = texture_artist_role_id
                ids.append(id)
            if roles == "Model Designer":
                id = model_designer_role_id
                ids.append(id)
            if roles == "App Developer":
                id = app_developer_role_id
                ids.append(id)
            if roles == "Bot Developer":
                id = bot_developer_role_id
                ids.append(id)
            if roles == "Datapack Developer":
                id = datapack_developer_role_id
                ids.append(id)
            if roles == "Plugin Developer":
                id = plugin_developer_role_id
                ids.append(id)
            if roles == "Mod Developer":
                id = mod_developer_role_id
                ids.append(id)
            if roles == "Forum Designer":
                id = forum_designer_role_id
                ids.append(id)
            if roles == "Pterodactyl Designer":
                id = pterodactyl_designer_role_id
                ids.append(id)
            if roles == "Store Designer":
                id = store_designer_role_id
                ids.append(id)
            if roles == "UIX Designer":
                id = uix_designer_role_id
                ids.append(id)
            if roles == "Web Designer":
                id = web_designer_role_id
                ids.append(id)
            if roles == "WIX Designer":
                id = wix_designer_role_id
                ids.append(id)
            if roles == "Configurator":
                id = configurator_role_id
                ids.append(id)
            if roles == "Discord Setup":
                id = discord_setup_role_id
                ids.append(id)
            if roles == "Forum Setup":
                id = forum_setup_role_id
                ids.append(id)
            if roles == "Server Setup":
                id = server_setup_role_id
                ids.append(id)
            if roles == "Store Setup":
                id = store_setup_role_id
                ids.append(id)
            if roles == "System Administrator":
                id = system_administrator_role_id
                ids.append(id)
            if roles == "Animator":
                id = animator_role_id
                ids.append(id)
            if roles == "Content Creator":
                id = content_creator_role_id
                ids.append(id)
            if roles == "Intro Creator":
                id = intro_creator_role_id
                ids.append(id)
            if roles == "Motion Designer":
                id = motion_designer_role_id
                ids.append(id)
            if roles == "Trailer Creator":
                id = trailer_creator_role_id
                ids.append(id)
            if roles == "Video Editor":
                id = video_editor_role_id
                ids.append(id)
            if roles == "Writer":
                id = writer_role_id
                ids.append(id)
            if roles == "Builder":
                id = builder_role_id
                ids.append(id)
            if roles == "Terraformer":
                id = terraformer_role_id
                ids.append(id)
            if roles == "Organic Builder":
                id = organic_builder_role_id
                ids.append(id)
            else:
                continue
        applicant = interaction.guild.get_member(a[0])
        for roles in ids:
            role = interaction.guild.get_role(roles)
            await applicant.add_roles(role)
        roles = (' \n'.join(self.values))
        r = roles.replace(", ", "\n")
        await db.execute('DELETE FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        valid_things = ("Commission Manager", "Application Reviewer", "Support Specialist")
        if any(thing in roles for thing in valid_things):
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
Welcome to the staff team! Please wait patiently until we give you more information about your position!
""", 
            color=discord.Color.from_str(embed_color))
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (accepted_application_payment, interaction.user.id))
            await e.edit(content=f'Accepted! You received **${accepted_application_payment:.2f}**!', view=None, embed=None)
        else:
            try:
                freelancer = interaction.guild.get_role(freelancer_role_id)
                await applicant.add_roles(freelancer)
            except:
                raise
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
If you haven't already, make sure to setup your profile. Use the command {freelancer_dashboard_command}> and click Profile to set up your profile!

You will start recieving commissions in the <#{freelancer_commission_channel_id}> channel. Please be sure to check <#{freelancer_announcement_channel_id}> frequently for any new announcements!
""", 
            color=discord.Color.from_str(embed_color))
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (accepted_application_payment, interaction.user.id))
            await e.edit(content=f'Accepted! You received **${accepted_application_payment:.2f}**!', view=None, embed=None)
        await db.commit()
        await db.close()

class ApplicationManagerDropdownView(discord.ui.View):
    def __init__(self, roles):
        super().__init__()
        self.roles = roles

        self.add_item(ApplicationManagerDropdown(roles))

class ApplicationManager(discord.ui.View):
    def __init__(self, ids):
        super().__init__(timeout=None)
        self.ids = ids

    @discord.ui.button(emoji='✅', label='Yes', style=discord.ButtonStyle.grey, custom_id='application:1')
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Accepting...", view=None, embed=None)
        e = await interaction.original_response()
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        try:
            channel = interaction.guild.get_channel(claim_ticket_channel_id)
            claim_message = channel.get_partial_message(a[3])
            await claim_message.delete()
        except:
            pass
        r = a[2].replace(", ", "\n")
        applicant = interaction.guild.get_member(a[0])
        for roles in self.ids:
            role = interaction.guild.get_role(roles)
            try:
                await applicant.add_roles(role)
            except:
                pass
        await db.execute('DELETE FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        valid_things = ("Commission Manager", "Application Reviewer", "Support Specialist")
        if any(thing in a[2] for thing in valid_things):
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
Welcome to the staff team! Please wait patiently until we give you more information about your position!
""", 
            color=discord.Color.from_str(embed_color))
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (accepted_application_payment, interaction.user.id))
            await e.edit(content=f'Accepted! You received **${accepted_application_payment:.2f}**!', view=None, embed=None)
        else:
            try:
                freelancer = interaction.guild.get_role(freelancer_role_id)
                await applicant.add_roles(freelancer)
            except:
                pass
            embed = discord.Embed(
                title="Application Accepted",
                description=f"""
Your application was accepted and you were given the following roles: ```
{r}
```
If you haven't already, make sure to setup your profile. Use the command {freelancer_dashboard_command} and click Profile to set up your profile!

You will start receiving commissions in the <#{freelancer_commission_channel_id}> channel. Please be sure to check <#{freelancer_announcement_channel_id}> frequently for any new announcements!
""", 
            color=discord.Color.from_str(embed_color))
            await interaction.channel.send(content=applicant.mention, embed=embed)
            await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (accepted_application_payment, interaction.user.id))
            await e.edit(content=f'Accepted! You received **${accepted_application_payment:.2f}**!', view=None, embed=None)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='❌', label='No', style=discord.ButtonStyle.grey, custom_id='application:2')
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        roles = a[2].split(", ")
        view = ApplicationManagerDropdownView(roles)
        await interaction.response.edit_message(content='Select the roles you would like to give them in the dropdown!', embed=None, view=view)

class ApplicationManager2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='✅', label='Accept', style=discord.ButtonStyle.grey, custom_id='application2:1')
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(description="This application has already been accepted or denied. Please get them to create a new apoplication if they wish to apply again!")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                ids = []
                x = a[2].split(", ")
                for roles in x:
                    if roles == "Commission Manager":
                        id = commission_manager_role_id
                        ids.append(id)
                    if roles == "Application Reviewer":
                        id = application_reviewer_role_id
                        ids.append(id)
                    if roles == "Support Specialist":
                        id = support_specialist_role_id
                        ids.append(id)
                    if roles == "Illustrator":
                        id = illustrator_role_id
                        ids.append(id)
                    if roles == "Vector Artist":
                        id = vector_artist_role_id
                        ids.append(id)
                    if roles == "GFX Designer":
                        id = gfx_designer_role_id
                        ids.append(id)
                    if roles == "Skin Designer":
                        id = skin_designer_role_id
                        ids.append(id)
                    if roles == "Render Artist":
                        id = render_artist_role_id
                        ids.append(id)
                    if roles == "Texture Arist":
                        id = texture_artist_role_id
                        ids.append(id)
                    if roles == "Model Designer":
                        id = model_designer_role_id
                        ids.append(id)
                    if roles == "App Developer":
                        id = app_developer_role_id
                        ids.append(id)
                    if roles == "Bot Developer":
                        id = bot_developer_role_id
                        ids.append(id)
                    if roles == "Datapack Developer":
                        id = datapack_developer_role_id
                        ids.append(id)
                    if roles == "Plugin Developer":
                        id = plugin_developer_role_id
                        ids.append(id)
                    if roles == "Mod Developer":
                        id = mod_developer_role_id
                        ids.append(id)
                    if roles == "Forum Designer":
                        id = forum_designer_role_id
                        ids.append(id)
                    if roles == "Pterodactyl Designer":
                        id = pterodactyl_designer_role_id
                        ids.append(id)
                    if roles == "Store Designer":
                        id = store_designer_role_id
                        ids.append(id)
                    if roles == "UIX Designer":
                        id = uix_designer_role_id
                        ids.append(id)
                    if roles == "Web Designer":
                        id = web_designer_role_id
                        ids.append(id)
                    if roles == "WIX Designer":
                        id = wix_designer_role_id
                        ids.append(id)
                    if roles == "Configurator":
                        id = configurator_role_id
                        ids.append(id)
                    if roles == "Discord Setup":
                        id = discord_setup_role_id
                        ids.append(id)
                    if roles == "Forum Setup":
                        id = forum_setup_role_id
                        ids.append(id)
                    if roles == "Server Setup":
                        id = server_setup_role_id
                        ids.append(id)
                    if roles == "Store Setup":
                        id = store_setup_role_id
                        ids.append(id)
                    if roles == "System Administrator":
                        id = system_administrator_role_id
                        ids.append(id)
                    if roles == "Animator":
                        id = animator_role_id
                        ids.append(id)
                    if roles == "Content Creator":
                        id = content_creator_role_id
                        ids.append(id)
                    if roles == "Intro Creator":
                        id = intro_creator_role_id
                        ids.append(id)
                    if roles == "Motion Designer":
                        id = motion_designer_role_id
                        ids.append(id)
                    if roles == "Trailer Creator":
                        id = trailer_creator_role_id
                        ids.append(id)
                    if roles == "Video Editor":
                        id = video_editor_role_id
                        ids.append(id)
                    if roles == "Writer":
                        id = writer_role_id
                        ids.append(id)
                    if roles == "Builder":
                        id = builder_role_id
                        ids.append(id)
                    if roles == "Terraformer":
                        id = terraformer_role_id
                        ids.append(id)
                    if roles == "Organic Builder":
                        id = organic_builder_role_id
                        ids.append(id)
                    else:
                        continue
                r = a[2].replace(", ", "\n")
                view = ApplicationManager(ids)
                embed=discord.Embed(
                description=f"Would you like to give the applicant all of the roles they applied for? Please use the buttons below. \n \n**__Roles__**: \n{r}", 
                color=discord.Color.from_str(embed_color))
                await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(emoji='❌', label='Deny', style=discord.ButtonStyle.grey, custom_id='application2:2')
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(description="This application has already been accepted or denied. Please get them to create a new application if they wish to apply again!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await db.execute('DELETE FROM applications WHERE channel_id=?', (interaction.channel.id, ))
                embed = discord.Embed(
                    title="Application Denied",
                    description="Unfortunately your application was denied because you don't meet the requirements for one or more of the positions you applied for.", 
                    color=discord.Color.red())
                await interaction.channel.send(content=f"<@{a[0]}>", embed=embed, view=None)
                embed = discord.Embed(
                    description="The application has been denied.", 
                    color=discord.Color.from_str(embed_color))
                await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (declined_application_payment, interaction.user.id))
                await interaction.response.edit_message(content=f'Denied. You received **${declined_application_payment:.2f}**!', embed=None, view=None)
            await db.commit()
            await db.close()

class ApplicationsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="application", description="Open the application manager view.")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def application(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This channel is either not an application channel or it has already been accepted/denied!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            cursor2 = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description=f"You must use the {freelancer_dashboard_command} command to use this command!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if a[4] != interaction.user.id:
                    embed = discord.Embed(description="You are not the application reviewer for this application!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    view = ApplicationManager2()
                    embed = discord.Embed(description="Do you accept or deny this application?", color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ApplicationsCog(bot), guilds=[discord.Object(id=guild_id)])