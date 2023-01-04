import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from typing import Optional

from src.freelancer.freelancer import FreelancerProfile

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class ProfileCog(commands.GroupCog, name="profile"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="view", description="View a user's profile!")
    @app_commands.describe(user="Who's profile would you like to view?")
    async def view(self, interaction: discord.Interaction, user: Optional[discord.Member]) -> None:
        db = await aiosqlite.connect('database.db')
        if user is None:
            user = interaction.user
        else:
            user = user
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message('That user does not have any information to view!', ephemeral=True)
        else:
            joined_at_timestamp = user.joined_at.timestamp()
            joined_at = int(joined_at_timestamp)
            if a[2] == 'null':
                title = "N/A"
            else:
                title = a[2]
            if a[3] == 'null':
                description = "N/A"
            else:
                description = a[3]
            if a[4] == 'null':
                portfolio = "N/A"
            else:
                portfolio = a[4]
            if a[5] == 'null':
                pronouns = "N/A"
            else:
                pronouns = a[5]
            if a[6] == 'null':
                timezone = "N/A"
            else:
                timezone = a[6]
            embed = discord.Embed(
                title="",
                color=discord.Color.from_str(embed_color))
            embed.add_field(name="Title", value=f"**{title}**", inline=True)
            embed.add_field(name="Description", value=f"**{description}**", inline=True)
            embed.add_field(name="Portfolio", value=f"**{portfolio}**", inline=True)
            embed.add_field(name="Pronouns", value=f"**{pronouns}**", inline=True)
            embed.add_field(name="Timezone", value=f"**{timezone}**", inline=True)
            embed.add_field(name="Joined", value=f"<t:{joined_at}:R>", inline=True)
            cursor2 = await db.execute('SELECT * from funds WHERE member_id=?', (user.id, ))
            b = await cursor2.fetchone()
            if b is None:
                pass
            else:
                embed.add_field(name="Commissions Completed", value=f"**{b[3]}**", inline=True)
                embed.add_field(name="Commissions Paid", value=f"**{b[4]}**", inline=True)
            embed.set_author(name=f"{user.name}'s Profile", icon_url=user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="setpaypalemail", description="Sets your paypal email link!")
    @app_commands.describe(email="What is your PayPal email?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def setpaypalemail(self, interaction: discord.Interaction, email: str):
        valid_options = ('@', 'null')
        if any(thing in email for thing in valid_options):
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, 0, 'null', 'null', 'null', 'null', 'null', email, 'null'))
                if email == 'null':
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal Email has been removed!",
                        color=discord.Color.from_str(embed_color))
                else:
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal Email has been set to **{email}**!",
                        color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await db.execute('UPDATE freelancer SET paypal=? WHERE freelancer_id=?', (email, interaction.user.id))
                if email == 'null':
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal Email has been removed!",
                        color=discord.Color.from_str(embed_color))
                else:
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal Email has been set to **{email}**!",
                        color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You must provide a valid email!", ephemeral=True)

    @app_commands.command(name="setpaypalme", description="Sets your paypal.me link!")
    @app_commands.describe(paypalme="What is your PayPal.me link?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def setpaypalme(self, interaction: discord.Interaction, paypalme: str):
        valid_options = ('paypal.me/', 'null')
        if any(thing in paypalme for thing in valid_options):
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, 0, 'null', 'null', 'null', 'null', 'null', 'null', paypalme))
                if paypalme == 'null':
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal.Me Link has been removed!",
                        color=discord.Color.from_str(embed_color))
                else:
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal Email has been set to **{paypalme}**!",
                        color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await db.execute('UPDATE freelancer SET paypal=? WHERE freelancer_id=?', (paypalme, interaction.user.id))
                if paypalme == 'null':
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal.Me Link has been removed!",
                        color=discord.Color.from_str(embed_color))
                else:
                    embed = discord.Embed(
                        title="Success",
                        description=f"Your PayPal.Me Link has been set to **{paypalme}**!",
                        color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await db.commit()
            await db.close()
        else:
            await interaction.response.send_message("You must provide a valid email!", ephemeral=True)

    @app_commands.command(name="settimezone", description="Sets your timezone!")
    @app_commands.describe(timezone="What is your Timezone?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def settimezone(self, interaction: discord.Interaction, timezone: str):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, 0, 'null', 'null', 'null', 'null', timezone, 'null', 'null'))
            if timezone == 'null':
                embed = discord.Embed(
                    title="Success",
                    description="Your Timezone has been removed!",
                    color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(
                    title="Success",
                    description=f"Your Timezone has been set to **{timezone}**!",
                    color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await db.execute('UPDATE freelancer SET timezone=? WHERE freelancer_id=?', (timezone, interaction.user.id))
            if timezone == 'null':
                embed = discord.Embed(
                    title="Success",
                    description="Your Timezone has been removed!",
                    color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(
                    title="Success",
                    description=f"Your Timezone has been set to **{timezone}**!",
                    color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="setpronouns", description="Sets your pronouns!")
    @app_commands.describe(pronouns="What are your pronouns?")
    @app_commands.guilds(discord.Object(id=guild_id))
    async def setpronouns(self, interaction: discord.Interaction, pronouns: str):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, 0, 'null', 'null', 'null', pronouns, 'null', 'null', 'null'))
            if pronouns == 'null':
                embed = discord.Embed(
                    title="Success",
                    description="Your Pronouns has been removed!",
                    color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(
                    title="Success",
                    description=f"Your Pronouns has been set to **{pronouns}**!",
                    color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await db.execute('UPDATE freelancer SET pronouns=? WHERE freelancer_id=?', (pronouns, interaction.user.id))
            if pronouns == 'null':
                embed = discord.Embed(
                    title="Success",
                    description="Your Pronouns has been removed!",
                    color=discord.Color.from_str(embed_color))
            else:
                embed = discord.Embed(
                    title="Success",
                    description=f"Your Pronouns has been set to **{pronouns}**!",
                    color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(ProfileCog(bot), guilds=[discord.Object(id=guild_id)])