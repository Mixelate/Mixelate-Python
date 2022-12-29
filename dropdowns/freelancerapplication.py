import discord
import yaml
from discord.ext import commands

from buttons.applications.freelancerapplicationsubmit import FreelancerApplicationSubmit

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class FreelancerApplicationDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='-------DESIGN-------'),
            discord.SelectOption(label='Illustrator'),
            discord.SelectOption(label='Vector Artist'),
            discord.SelectOption(label='GFX Designer'),
            discord.SelectOption(label='Skin Designer'),
            discord.SelectOption(label='Render Artist'),
            discord.SelectOption(label='Texture Artist'),
            discord.SelectOption(label='Model Designer'),
            discord.SelectOption(label='-------DEVELOPMENT-------'),
            discord.SelectOption(label='App Developer'),
            discord.SelectOption(label='Bot Developer'),
            discord.SelectOption(label='Datapack Developer'),
            discord.SelectOption(label='Plugin Developer'),
            discord.SelectOption(label='Mod Developer'),
            discord.SelectOption(label='-------WEB-------'),
            discord.SelectOption(label='Forum Designer'),
            discord.SelectOption(label='Pterodactyl Designer'),
            discord.SelectOption(label='Store Designer'),
            discord.SelectOption(label='UIX Designer'),
            discord.SelectOption(label='Web Designer'),
            discord.SelectOption(label='Web Developer'),
            discord.SelectOption(label='Wix Designer'),
        ]

        super().__init__(placeholder="Choose all the roles you're applying for!", min_values=1, max_values=19, options=options)

    async def callback(self, interaction: discord.Interaction):
        remove = {'-------DESIGN-------', '-------DEVELOPMENT-------', '-------WEB-------'}
        values = [ x for x in self.values if x not in remove ]
        self.view.stored_values = values
        stored_roles = (', '.join(values))
        self.view.stored_roles = stored_roles
        roles = (' \n'.join(values))
        self.view.roles = roles
        if roles == '':
            embed = discord.Embed(title="Freelancer Applications",
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
Wix Designer""",
            color=discord.Color.from_str(embed_color))
            await interaction.response.edit_message(embed=embed)
        else:
            embed = discord.Embed(title="Freelancer Applications", 
            description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*{roles}*

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
            await interaction.response.edit_message(embed=embed)

class FreelancerApplicationDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.stored_roles = None
        self.roles = None
        self.stored_values = None

        self.add_item(FreelancerApplicationDropdown())
        self.add_item(FreelancerApplicationSubmit())
        self.add_item(FreelancerApplicationNext())

class FreelancerApplicationDropdownTwo(discord.ui.Select):
    def __init__(self, stored_values, stored_roles, roles):
        self.stored_values = stored_values
        self.stored_roles = stored_roles
        self.roles = roles

        options = [
            discord.SelectOption(label='-------SETUPS-------'),
            discord.SelectOption(label='Configurator'),
            discord.SelectOption(label='Discord Setup'),
            discord.SelectOption(label='Forum Setup'),
            discord.SelectOption(label='Server Setup'),
            discord.SelectOption(label='Store Setup'),
            discord.SelectOption(label='System Administrator'),
            discord.SelectOption(label='-------VIDEO-------'),
            discord.SelectOption(label='Animator'),
            discord.SelectOption(label='Trailer Creator'),
            discord.SelectOption(label='Video Editor'),
            discord.SelectOption(label='Motion Designer'),
            discord.SelectOption(label='Intro Creator'),
            discord.SelectOption(label='Content Creator'),
            discord.SelectOption(label='-------CREATIVE-------'),
            discord.SelectOption(label='Builder'),
            discord.SelectOption(label='Organic Builder'),
            discord.SelectOption(label='Terraformer'),
            discord.SelectOption(label='Writer'),
        ]

        super().__init__(placeholder="Choose all the roles you're applying for!", min_values=1, max_values=16, options=options)

    async def callback(self, interaction: discord.Interaction):
        remove = {'-------SETUPS-------', '-------VIDEO-------', '-------CREATIVE-------'}
        values = [ x for x in self.values if x not in remove ]
        if self.stored_roles == '':
            del self.stored_roles
            del self.stored_values
        if values == []:
            embed = discord.Embed(title="Freelancer Applications", 
            description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*N/A*

**Setups**
Configurator
Discord Setup
Forum Setup
Server Setup
Store Setup
System Administrator

**Video**
Animator
Trailer Creator
Video Editor
Motion Designer
Intro Creator
Content Creator

**Creative**
Builder
Organic Builder
Terraformer
Writer
""", 
            color=discord.Color.from_str(embed_color))
        else:
            try:
                self.view.roles = (' \n'.join(self.stored_values)) + '\n' + (' \n'.join(values))
            except:
                self.view.roles = (' \n'.join(values))
            try:
                self.view.stored_values = self.stored_values + values
            except:
                self.view.stored_values = values
            try:
                self.view.stored_roles = self.stored_roles + ', ' + (', '.join(values))
            except:
                self.view.stored_roles = (', '.join(values))

            embed = discord.Embed(title="Freelancer Applications", 
            description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*{self.view.roles}*

**Setups**
Configurator
Discord Setup
Forum Setup
Server Setup
Store Setup
System Administrator

**Video**
Animator
Trailer Creator
Video Editor
Motion Designer
Intro Creator
Content Creator

**Creative**
Builder
Organic Builder
Terraformer
Writer
""", 
            color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed)

class FreelancerApplicationDropdownViewTwo(discord.ui.View):
    def __init__(self, stored_values, stored_roles, roles):
        super().__init__()
        self.stored_values = stored_values
        self.stored_roles = stored_roles
        self.roles = roles

        self.stored_values2 = None
        self.stored_roles2 = None
        self.roles2 = None

        self.add_item(FreelancerApplicationDropdownTwo(stored_values, stored_roles, roles))
        self.add_item(FreelancerApplicationSubmit())
        self.add_item(FreelancerApplicationRestart())

class FreelancerApplicationNext(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Next Page', emoji='➡️')

    async def callback(self, interaction: discord.Interaction):
        stored_values = self.view.stored_values
        stored_roles = self.view.stored_roles
        roles = self.view.roles
        view = FreelancerApplicationDropdownViewTwo(stored_values, stored_roles, roles)
        if roles == None:
            roles = "N/A"
        if roles == '':
            embed = discord.Embed(title="Freelancer Applications", 
            description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*N/A*

**Setups**
Configurator
Discord Setup
Forum Setup
Server Setup
Store Setup
System Administrator

**Video**
Animator
Trailer Creator
Video Editor
Motion Designer
Intro Creator
Content Creator

**Creative**
Builder
Organic Builder
Terraformer
Writer
""", 
            color=discord.Color.from_str(embed_color))
        else:
            embed = discord.Embed(title="Freelancer Applications", 
            description=f"""
Please select all the roles you are applying for. You may select as many as you qualify for!

**Chosen Roles:**
*{roles}*

**Setups**
Configurator
Discord Setup
Forum Setup
Server Setup
Store Setup
System Administrator

**Video**
Animator
Trailer Creator
Video Editor
Motion Designer
Intro Creator
Content Creator

**Creative**
Builder
Organic Builder
Terraformer
Writer
""", 
            color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed, view=view)

class FreelancerApplicationRestart(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Restart', emoji='🔁')

    async def callback(self, interaction: discord.Interaction):

        view = FreelancerApplicationDropdownView()

        embed = discord.Embed(title="Freelancer Applications", 
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

class FreelancerApplicationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(FreelancerApplicationCog(bot), guilds=[discord.Object(id=guild_id)])