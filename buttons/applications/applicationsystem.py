import discord
import yaml
from discord.ext import commands

from dropdowns.freelancerapplication import FreelancerApplicationDropdownView
from dropdowns.staffapplication import StaffApplicationDropdownView

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class ApplicationSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='⚒️', label='Freelancer', style=discord.ButtonStyle.grey, custom_id='applications:1')
    async def freelancer(self, interaction: discord.Interaction, button: discord.ui.Button):

        view = FreelancerApplicationDropdownView()

        embed=discord.Embed(title="Freelancer Applications", 
        description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*N/A*

**Design**
Illustrator
Vector Artist
GFX Designer
Skin Designer
Render Artist
Texture Artist
Model Designer

**Development**
App Developer
Bot Developer
Datapack Developer
Plugin Developer
Mod Developer

**Web**
Forum Designer
Pterodactyl Designer
Store Designer
UIX Designer
Web Designer
Web Developer
Wix Designer
""", 
        color=discord.Color.from_str(embed_color))

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(emoji='🛠️', label='Staff', style=discord.ButtonStyle.grey, custom_id='applications:2')
    async def staff(self, interaction: discord.Interaction, button: discord.ui.Button):

        view = StaffApplicationDropdownView()

        embed=discord.Embed(title="Staff Applications", 
        description=f"Please select a role that you're applying for!",
        color=discord.Color.from_str(embed_color))

        await interaction.response.edit_message(embed=embed, view=view)

class ApplicationSystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(ApplicationSystemCog(bot), guilds=[discord.Object(id=guild_id)])