import discord
import asyncio
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)
embed_color = data["General"]["EMBED_COLOR"]

class HelpPaginator(discord.ui.View):
    def __init__(self, page, interaction):
        super().__init__(timeout=60)
        self.page = page
        self.interaction = interaction
        self.response = None

    async def on_timeout(self):
        try:
            for child in self.children:
                child.disabled = True
            await self.response.edit(view=self)
        except:
            return

    async def interaction_check(self, interaction):
        if interaction.user == self.interaction.user:
            return True
        else:
            embed = discord.Embed(
                title="ERROR",
                description="This menu is not for you!",
                color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(emoji='<:first:1033564178667032656>', style=discord.ButtonStyle.blurple, custom_id='first')
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        all_items = self.children
        w = discord.utils.get(all_items, custom_id="first")
        x = discord.utils.get(all_items, custom_id="back")
        w.disabled = True
        x.disabled = True
        if self.page == 5:
            y = discord.utils.get(all_items, custom_id="last")
            z = discord.utils.get(all_items, custom_id="next")
            y.disabled = False
            z.disabled = False
        self.page = 1
        embed = discord.Embed(
                description="""
</addaccess:1042236164876275734>
<:reply:1042628467335888926> Adds someone to the ticket you're in

</close:1042236164876275736>
<:reply:1042628467335888926> Closes the ticket you're in

</freelancer balance:1042215472092958771>
<:reply:1042628467335888926> Shows you how much money you have

</freelancer dashboard:1042215472092958771>
<:reply:1042628467335888926> Opens the freelancer's main dashboard

</help:1042627857949659257>
<:reply:1042628467335888926> Shows you all the available commands

</latency:1042218688490770462>
<:reply:1042628467335888926> Shows you the bot's latency

</ping:1042218688490770464>
<:reply:1042628467335888926> Shows you the bot's ping

</removeaccess:1042236164876275735>
<:reply:1042628467335888926> Removes someone from the ticket you're in
""",
            color=discord.Color.from_str(embed_color))
        embed.set_footer(text=f"Page 1 of 5")
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(emoji='<:back:1033564166813909072>', style=discord.ButtonStyle.blurple, custom_id='back')
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        all_items = self.children
        self.page = self.page - 1
        if self.page == 4:
            y = discord.utils.get(all_items, custom_id="last")
            z = discord.utils.get(all_items, custom_id="next")
            y.disabled = False
            z.disabled = False
            embed = discord.Embed(
                description="""
Coming Soon!
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 4 of 5")

        if self.page == 3:
            embed = discord.Embed(
                description="""
Coming Soon!
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 3 of 5")

        if self.page == 2:
            embed = discord.Embed(
                description="""
</tickets:1042236164876275733>
<:reply:1042628467335888926> Sends the ticket panel

</uptime:1042218688490770463>
<:reply:1042628467335888926> Shows you the bot's uptime

</view freelancer:1042215472092958772>
<:reply:1042628467335888926> Shows you information about a freelancer
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 2 of 5")

        if self.page == 1:
            y = discord.utils.get(all_items, custom_id="back")
            z = discord.utils.get(all_items, custom_id="first")
            y.disabled = True
            z.disabled = True
            embed = discord.Embed(
                description="""
</addaccess:1042236164876275734>
<:reply:1042628467335888926> Adds someone to the ticket you're in

</close:1042236164876275736>
<:reply:1042628467335888926> Closes the ticket you're in

</freelancer balance:1042215472092958771>
<:reply:1042628467335888926> Shows you how much money you have

</freelancer dashboard:1042215472092958771>
<:reply:1042628467335888926> Opens the freelancer's main dashboard

</help:1042627857949659257>
<:reply:1042628467335888926> Shows you all the available commands

</latency:1042218688490770462>
<:reply:1042628467335888926> Shows you the bot's latency

</ping:1042218688490770464>
<:reply:1042628467335888926> Shows you the bot's ping

</removeaccess:1042236164876275735>
<:reply:1042628467335888926> Removes someone from the ticket you're in
""",
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 1 of 5")
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(emoji='<:next:1033564190104891462>', style=discord.ButtonStyle.blurple, custom_id='next')
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.page = self.page + 1
        if self.page == 2:
            all_items = self.children
            y = discord.utils.get(all_items, custom_id="first")
            z = discord.utils.get(all_items, custom_id="back")
            y.disabled = False
            z.disabled = False
            embed = discord.Embed(
                description="""
</tickets:1042236164876275733>
<:reply:1042628467335888926> Sends the ticket panel

</uptime:1042218688490770463>
<:reply:1042628467335888926> Shows you the bot's uptime

</view freelancer:1042215472092958772>
<:reply:1042628467335888926> Shows you information about a freelancer
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 2 of 5")
        if self.page == 3:
            embed = discord.Embed(
                description="""
Coming Soon!
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 3 of 5")
        if self.page == 4:
            embed = discord.Embed(
                description="""
Coming Soon!
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 4 of 5")
        if self.page == 5:
            all_items = self.children
            y = discord.utils.get(all_items, custom_id="next")
            z = discord.utils.get(all_items, custom_id="last")
            y.disabled = True
            z.disabled = True
            embed = discord.Embed(
                description="""
Coming Soon!
""", 
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=f"Page 5 of 5")
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(emoji='<:last:1033564204109664318>', style=discord.ButtonStyle.blurple, custom_id='last')
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        all_items = self.children
        if self.page == 1:
            y = discord.utils.get(all_items, custom_id="first")
            z = discord.utils.get(all_items, custom_id="back")
            y.disabled = False
            z.disabled = False
        self.page = 5
        w = discord.utils.get(all_items, custom_id="next")
        x = discord.utils.get(all_items, custom_id="last")
        w.disabled = True
        x.disabled = True
        embed = discord.Embed(
                description="""
Coming Soon!
""", 
            color=discord.Color.from_str(embed_color))
        embed.set_footer(text=f"Page 5 of 5")
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(emoji='❌', style=discord.ButtonStyle.blurple, custom_id='close')
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(view=self)
        await asyncio.sleep(5)
        await interaction.message.delete()

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="help", description="See the list of all available commands!")
    async def help(self, interaction: discord.Interaction) -> None:
        page = 1
        view = HelpPaginator(page, interaction)
        view.first.disabled = True
        view.back.disabled = True
        embed = discord.Embed(
            description="""
</addaccess:1042236164876275734>
<:reply:1042628467335888926> Adds someone to the ticket you're in

</close:1042236164876275736>
<:reply:1042628467335888926> Closes the ticket you're in

</freelancer balance:1042215472092958771>
<:reply:1042628467335888926> Shows you how much money you have

</freelancer dashboard:1042215472092958771>
<:reply:1042628467335888926> Opens the freelancer's main dashboard

</help:1042627857949659257>
<:reply:1042628467335888926> Shows you all the available commands

</latency:1042218688490770462>
<:reply:1042628467335888926> Shows you the bot's latency

</ping:1042218688490770464>
<:reply:1042628467335888926> Shows you the bot's ping

</removeaccess:1042236164876275735>
<:reply:1042628467335888926> Removes someone from the ticket you're in
""",
            color=discord.Color.from_str(embed_color))
        embed.set_footer(text="Page 1 of 5")
        await interaction.response.send_message(embed=embed, view=view)
        message = await interaction.original_response()
        view.response = message

async def setup(bot):
    await bot.add_cog(HelpCog(bot))