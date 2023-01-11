import discord
import aiosqlite
import datetime as DT
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Optional
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class Reviews(discord.ui.View):
    def __init__(self, user, page):
        super().__init__(timeout=None)
        self.user = user
        self.page = page

    @discord.ui.button(emoji='<:first:1033564178667032656>', style=discord.ButtonStyle.grey, custom_id='reviews:1')
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE freelancer_id=?', (self.user.id,))
        a = await cursor.fetchall()
        amount = 0
        for i in a:
            amount += 1
        self.page = 1
        page = self.page-1
        view = Reviews(self.user, self.page)
        view.last.disabled = False
        view.next.disabled = False
        if self.page == 1:
            view.first.disabled = True
            view.back.disabled = True
        member = interaction.guild.get_member(a[page][1])
        service = interaction.guild.get_role(a[page][3])
        embed = discord.Embed(title=f"Review from {member}", color=discord.Color.from_str(embed_color))
        if a[page][5] == 1:
            rating = "⭐ (1.0)"
        if a[page][5] == 2:
            rating = "⭐⭐ (2.0)"
        if a[page][5] == 3:
            rating = "⭐⭐⭐ (3.0)"
        if a[page][5] == 4:
            rating = "⭐⭐⭐⭐ (4.0)"
        if a[page][5] == 5:
            rating = "⭐⭐⭐⭐⭐ (5.0)"
        embed.add_field(name="Rating", value=rating, inline=False)
        embed.add_field(name="Service", value=service.mention, inline=False)
        embed.add_field(name="Review", value=a[page][4], inline=False)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        timestamp = datetime.fromtimestamp(a[page][6])
        embed.timestamp = timestamp
        await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='<:back:1033564166813909072>', style=discord.ButtonStyle.grey, custom_id='reviews:2')
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE freelancer_id=?', (self.user.id,))
        a = await cursor.fetchall()
        amount = 0
        for i in a:
            amount += 1
        self.page = self.page-1
        page = self.page-1
        view = Reviews(self.user, self.page)
        view.last.disabled = False
        view.next.disabled = False
        if self.page == 1:
            view.first.disabled = True
            view.back.disabled = True
        member = interaction.guild.get_member(a[page][1])
        service = interaction.guild.get_role(a[page][3])
        if a[page][5] == 1:
            rating = "⭐ (1.0)"
        if a[page][5] == 2:
            rating = "⭐⭐ (2.0)"
        if a[page][5] == 3:
            rating = "⭐⭐⭐ (3.0)"
        if a[page][5] == 4:
            rating = "⭐⭐⭐⭐ (4.0)"
        if a[page][5] == 5:
            rating = "⭐⭐⭐⭐⭐ (5.0)"
        embed = discord.Embed(title=f"Review from {member}", color=discord.Color.from_str(embed_color))
        embed.add_field(name="Rating", value=rating, inline=False)
        embed.add_field(name="Service", value=service.mention, inline=False)
        embed.add_field(name="Review", value=a[page][4], inline=False)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        timestamp = datetime.fromtimestamp(a[page][6])
        embed.timestamp = timestamp
        await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='<:next:1033564190104891462>', style=discord.ButtonStyle.grey, custom_id='reviews:3')
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE freelancer_id=?', (self.user.id,))
        a = await cursor.fetchall()
        amount = 0
        for i in a:
            amount += 1
        self.page = self.page+1
        page = self.page-1
        view = Reviews(self.user, self.page)
        view.first.disabled = False
        view.back.disabled = False
        if self.page == amount:
            view.next.disabled = True
            view.last.disabled = True
        member = interaction.guild.get_member(a[page][1])
        service = interaction.guild.get_role(a[page][3])
        embed = discord.Embed(title=f"Review from {member}", color=discord.Color.from_str(embed_color))
        if a[page][5] == 1:
            rating = "⭐ (1.0)"
        if a[page][5] == 2:
            rating = "⭐⭐ (2.0)"
        if a[page][5] == 3:
            rating = "⭐⭐⭐ (3.0)"
        if a[page][5] == 4:
            rating = "⭐⭐⭐⭐ (4.0)"
        if a[page][5] == 5:
            rating = "⭐⭐⭐⭐⭐ (5.0)"
        embed.add_field(name="Rating", value=rating, inline=False)
        embed.add_field(name="Service", value=service.mention, inline=False)
        embed.add_field(name="Review", value=a[page][4], inline=False)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        timestamp = datetime.fromtimestamp(a[page][6])
        embed.timestamp = timestamp
        await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='<:last:1033564204109664318>', style=discord.ButtonStyle.grey, custom_id='reviews:4')
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE freelancer_id=?', (self.user.id,))
        a = await cursor.fetchall()
        amount = 0
        for i in a:
            amount += 1
        self.page = amount-1
        page = amount
        view = Reviews(self.user, page)
        view.first.disabled = False
        view.back.disabled = False
        view.next.disabled = True
        view.last.disabled = True
        member = interaction.guild.get_member(a[self.page][1])
        service = interaction.guild.get_role(a[self.page][3])
        embed = discord.Embed(title=f"Review from {member}", color=discord.Color.from_str(embed_color))
        if a[self.page][5] == 1:
            rating = "⭐ (1.0)"
        if a[self.page][5] == 2:
            rating = "⭐⭐ (2.0)"
        if a[self.page][5] == 3:
            rating = "⭐⭐⭐ (3.0)"
        if a[self.page][5] == 4:
            rating = "⭐⭐⭐⭐ (4.0)"
        if a[self.page][5] == 5:
            rating = "⭐⭐⭐⭐⭐ (5.0)"
        embed.add_field(name="Rating", value=rating, inline=False)
        embed.add_field(name="Service", value=service.mention, inline=False)
        embed.add_field(name="Review", value=a[self.page][4], inline=False)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        timestamp = datetime.fromtimestamp(a[self.page][6])
        embed.timestamp = timestamp
        await interaction.response.edit_message(embed=embed, view=view)
        await db.commit()
        await db.close()

class ReviewsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="reviews", description="Shows you the reviews of someone!")
    @app_commands.describe(member="Who's reviews would you like to view?")
    async def reviews(self, interaction: discord.Interaction, member: Optional[discord.Member]) -> None:
        if member is None:
            user = interaction.user
        else:
            user = member
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE freelancer_id=?', (user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"{user.mention} does not have any reviews available!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            cursor = await db.execute('SELECT * from reviews WHERE freelancer_id=?', (user.id,))
            a = await cursor.fetchall()
            amount = 0
            page = 1
            for i in a:
                amount += 1
            view = Reviews(user, page)
            view.first.disabled = True
            view.back.disabled = True
            if amount == 1:
                view.next.disabled = True
                view.last.disabled = True
            member = interaction.guild.get_member(a[0][1])
            service = interaction.guild.get_role(a[0][3])
            if a[0][5] == 1:
                rating = "⭐ (1.0)"
            if a[0][5] == 2:
                rating = "⭐⭐ (2.0)"
            if a[0][5] == 3:
                rating = "⭐⭐⭐ (3.0)"
            if a[0][5] == 4:
                rating = "⭐⭐⭐⭐ (4.0)"
            if a[0][5] == 5:
                rating = "⭐⭐⭐⭐⭐ (5.0)"
            embed = discord.Embed(title=f"Review from {member}", color=discord.Color.from_str(embed_color))
            embed.add_field(name="Rating", value=rating, inline=False)
            embed.add_field(name="Service", value=service.mention, inline=False)
            embed.add_field(name="Review", value=a[0][4], inline=False)
            embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
            timestamp = datetime.fromtimestamp(a[0][6])
            embed.timestamp = timestamp
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(ReviewsCog(bot), guilds=[discord.Object(id=guild_id)])