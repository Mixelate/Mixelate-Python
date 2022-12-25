import discord
import yaml
from discord.ext import commands

from modals.support import Support
from buttons.applications.applicationsystem import ApplicationSystem
from dropdowns.order.orderdropdown import OrderDropdownView

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
freelancer_commission_channel_id = data["Tickets"]["FREELANCER_COMMISSION_CHANNEL_ID"]
staff_claim_ticket_channel_id = data["Tickets"]["STAFF_CLAIM_TICKET_CHANNEL_ID"]
transcripts_channel_id = data["Tickets"]["TRANSCRIPTS_CHANNEL_ID"]

class TicketSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='🛒', label='Order', style=discord.ButtonStyle.grey, custom_id='tickets:1')
    async def order(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed=discord.Embed(title="Choose a Commission Category", 
        description="""
**Design**
Illustrator, Model Designer, Texture Artist, Render Artist, Skin Designer, GFX Designer, Vector Artist

**Development**
Bot Developer, Datapack Developer, Plugin Developer, Mod Developer, App Developer

**Web**
Forum Designer, Pterodactyl Designer, Store Designer, UIX Designer, Web Designer, Web Developer, Wix Designer

**Setups**
Configurator, Discord Setup, Forum Setup, Server Setup, Store Setup, System Administrator

**Video**
Animator, Trailer Creator, Video Editor, Motion Designer, Intro Creator, Content Creator

**Creative**
Builder, Organic Builder, Terraformer, Writer
""", 
        color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, view=OrderDropdownView(), ephemeral=True)

    @discord.ui.button(emoji='⚒️', label='Applications', style=discord.ButtonStyle.grey, custom_id='tickets:3')
    async def applications(self, interaction: discord.Interaction, button: discord.ui.Button):

        view = ApplicationSystem()

        embed=discord.Embed(title="", 
        description=f"Please select the category you're applying for!", 
        color=discord.Color.from_str(embed_color))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(emoji='✉️', label='Support', style=discord.ButtonStyle.grey, custom_id='tickets:2')
    async def support(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(Support())

class TicketSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(TicketSystem())

async def setup(bot):
    await bot.add_cog(TicketSystemCog(bot), guilds=[discord.Object(id=guild_id)])