import discord
import aiosqlite
import yaml
import datetime as DT
from datetime import datetime

from buttons.freelancer.freelancersystem import FreelancerSystem
from buttons.commissions.claimcommissionticket import ClaimCommissionTicket
from buttons.tickets.ticketclose import TicketClose

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
commission_ticket_category_id = data["Tickets"]["COMMISSION_TICKET_CATEGORY_ID"]
freelancer_commission_channel_id = data["Tickets"]["FREELANCER_COMMISSION_CHANNEL_ID"]
staff_claim_ticket_channel_id = data["Tickets"]["STAFF_CLAIM_TICKET_CHANNEL_ID"]
commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]

illustrator_role_id = data["Freelancer_Roles"]["ILLUSTRATOR_ROLE_ID"]
vector_artist_role_id = data["Freelancer_Roles"]["VECTOR_ARTIST_ROLE_ID"]
gfx_designer_role_id = data["Freelancer_Roles"]["GFX_DESIGNER_ROLE_ID"]
skin_designer_role_id = data["Freelancer_Roles"]["SKIN_DESIGNER_ROLE_ID"]
render_artist_role_id = data["Freelancer_Roles"]["RENDER_ARTIST_ROLE_ID"]
texture_artist_role_id = data["Freelancer_Roles"]["TEXTURE_ARTIST_ROLE_ID"]
model_designer_role_id= data["Freelancer_Roles"]["MODEL_DESIGNER_ROLE_ID"]
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

class Order(discord.ui.Modal, title='Order Services'):
    def __init__(self, category):
        super().__init__(timeout=None)
        self.category = category
    
        if self.category == "Illustrator":
            self.role_id = illustrator_role_id
        if self.category == "Model Designer":
            self.role_id = model_designer_role_id
        if self.category == "Texture Artist":
            self.role_id = texture_artist_role_id
        if self.category == "Render Artist":
            self.role_id = render_artist_role_id
        if self.category == "Skin Designer":
            self.role_id = skin_designer_role_id
        if self.category == "GFX Designer":
            self.role_id = gfx_designer_role_id
        if self.category == "Vector Artist":
            self.role_id = vector_artist_role_id
        if self.category == "Bot Developer":
            self.role_id = bot_developer_role_id
        if self.category == "Datapack Developer":
            self.role_id = datapack_developer_role_id
        if self.category == "Plugin Developer":
            self.role_id = plugin_developer_role_id
        if self.category == "Mod Developer":
            self.role_id = mod_developer_role_id
        if self.category == "App Developer":
            self.role_id = app_developer_role_id
        if self.category == "Forum Designer":
            self.role_id = forum_designer_role_id
        if self.category == "Pterodactyl Designer":
            self.role_id = pterodactyl_designer_role_id
        if self.category == "Store Designer":
            self.role_id = store_designer_role_id
        if self.category == "UIX Designer":
            self.role_id = uix_designer_role_id
        if self.category == "Web Designer":
            self.role_id = web_designer_role_id
        if self.category == "Web Developer":
            self.role_id = web_developer_role_id
        if self.category == "WIX Designer":
            self.role_id = wix_designer_role_id
        if self.category == "Configurator":
            self.role_id = configurator_role_id
        if self.category == "Discord Setup":
            self.role_id = discord_setup_role_id
        if self.category == "Forum Setup":
            self.role_id = forum_setup_role_id
        if self.category == "Server Setup":
            self.role_id = server_setup_role_id
        if self.category == "Store Setup":
            self.role_id = store_setup_role_id
        if self.category == "System Administrator":
            self.role_id = system_administrator_role_id
        if self.category == "Animator":
            self.role_id = animator_role_id
        if self.category == "Trailer Creator":
            self.role_id = trailer_creator_role_id
        if self.category == "Video Editor":
            self.role_id = video_editor_role_id
        if self.category == "Motion Designer":
            self.role_id = motion_designer_role_id
        if self.category == "Intro Creator":
            self.role_id = intro_creator_role_id
        if self.category == "Content Creator":
            self.role_id = content_creator_role_id
        if self.category == "Builder":
            self.role_id = builder_role_id
        if self.category == "Organic Builder":
            self.role_id = organic_builder_role_id
        if self.category == "Terraformer":
            self.role_id = terraformer_role_id
        if self.category == "Writer":
            self.role_id = writer_role_id

    budget = discord.ui.TextInput(
        label='Budget',
        placeholder='What is your budget?',
        max_length=5,
    )

    deadline = discord.ui.TextInput(
        label='Deadline',
        placeholder='What is your deadline?',
        max_length=25,
    )

    description = discord.ui.TextInput(
        label='Project Description',
        style=discord.TextStyle.long,
        placeholder='What is your project description?',
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content='Creating...', embed=None, view=None)
        db = await aiosqlite.connect('database.db')

        category_channel = interaction.guild.get_channel(commission_ticket_category_id)
        ticket_channel = await category_channel.create_text_channel(
            f"order-{interaction.user.name}")
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

        commissions_channel = interaction.guild.get_channel(freelancer_commission_channel_id)

        embed = discord.Embed(title="New Commission",
            description=f"""
**__Budget__**
{self.budget.value}

**__Deadline__**
{self.deadline.value}

**__Project Description__**
{self.description.value}
""",
            color=discord.Color.from_str(embed_color))
        
        embed.set_footer(text="Mixelate", icon_url=interaction.guild.icon.url)
        embed.timestamp = datetime.now()

        role = interaction.guild.get_role(self.role_id)

        c = await commissions_channel.send(content=f'{role.mention}', embed=embed, view=FreelancerSystem())

        claim_channel = interaction.guild.get_channel(staff_claim_ticket_channel_id)
        commission_manager = interaction.guild.get_role(commission_manager_role_id)

        a = DT.datetime.now().timestamp()
        b = int(a)

        embed=discord.Embed( 
        description=f"""
**Commission <t:{b}:R>**
```
Commission Deadline: {self.deadline.value}
Commission Details: {self.description.value}
```
""",
        color=discord.Color.from_str(embed_color))

        view = ClaimCommissionTicket()

        d = await claim_channel.send(content=commission_manager.mention, embed=embed, view=view)

        await db.execute('INSERT INTO commissions VALUES (?,?,?,?,?,?,?,?,?,?);', (ticket_channel.id, self.role_id, c.id, 'null', 'null', d.id, 'null', self.budget.value, self.deadline.value, self.description.value))

        x = f'{interaction.user.mention}'

        embed = discord.Embed(title="Order Information",
                            description=f"""
Our freelancers will begin sending you quotes for your project shortly. You will be notified when you receive a response!

**Some Tips While You Wait** ```
- If you have any issues during the commission process try pinging the commission manager! 

- Did you and the freelancer decide on a new price? The price can be updated any time before paying by clicking "Confirm" when prompted!```

**Details** ```
Budget: {self.budget.value}

Deadline: {self.deadline.value}

Project Description: {self.description.value}```
""",
                            color=discord.Color.from_str(embed_color))

        view = TicketClose()

        await ticket_channel.send(content=x, embed=embed, view=view)

        await interaction.edit_original_response(content=f'The ticket has been created at {ticket_channel.mention}.')

        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)