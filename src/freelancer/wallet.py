import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

from buttons.wallet.wallet import Wallet

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
payout_channel_id = data["Freelancer"]["PAYOUT_CHANNEL_ID"]

class RequestPayout(discord.ui.Modal, title='Requesting Your Payout!'):

    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    setpaypal = discord.ui.TextInput(
        label='Requesting Payout',
        placeholder='What is your PayPal email?',
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if "@" in self.setpaypal.value:
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
            a = await cursor.fetchone()
            if a is None:
                await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, 0, 'null' 'null', 'null', 'null', 'null', self.setpaypal.value, 'null'))
                await interaction.response.send_message("You cannot request for a payout as you do not have a profile setup!", ephemeral=True)
            else:
                await db.execute('UPDATE freelancer SET paypal=? WHERE freelancer_id=?', (self.setpaypal.value, interaction.user.id))
                await db.execute('UPDATE freelancer SET balance=balance-? WHERE freelancer_id=?', (self.amount, interaction.user.id))
                embed = discord.Embed(
                    title="",
                    description=f"Your PayPal has been set to **{self.setpaypal.value}** and the request has been sent.",
                    color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
                payout_channel = interaction.guild.get_channel(payout_channel_id)
                embed = discord.Embed(
                    title="",
                    color=discord.Color.from_str(embed_color))
                embed.add_field(name="PayPal", value=f"**{self.setpaypal.value}**", inline=True)
                embed.add_field(name="Amount", value=f"**${self.amount:.2f}**", inline=True)
                await payout_channel.send(content=f"{interaction.user.mention} ({interaction.user.id}) has requested for a payout!", embed=embed, view=None)
            await db.commit()
            await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class WalletCog(commands.GroupCog, name="wallet"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="withdraw", description="Withdraw funds!")
    @app_commands.describe(amount="How much would you like to withdraw?")
    async def withdraw(self, interaction: discord.Interaction, amount: int) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message('You do not have a freelancer profile set!', ephemeral=True)
        else:
            if amount > a[1] or amount == 0:
                await interaction.response.send_message('You cannot withdraw more than you have!', ephemeral=True)
            else:
                if a[7] == 'null':
                    await interaction.response.send_modal(RequestPayout(amount))
                else:
                    await db.execute('UPDATE freelancer SET balance=balance-? WHERE freelancer_id=?', (amount, interaction.user.id))
                    payout_channel = interaction.guild.get_channel(payout_channel_id)
                    embed = discord.Embed(
                        title="",
                        color=discord.Color.from_str(embed_color))
                    embed.add_field(name="PayPal", value=f"**{a[7]}**", inline=True)
                    embed.add_field(name="Amount", value=f"**${amount:.2f}**", inline=True)
                    await payout_channel.send(content=f"{interaction.user.mention} ({interaction.user.id}) has requested for a payout!", embed=embed)
                    await interaction.response.send_message(content="You have successfully requested your payout! The money will be transferred to your PayPal soon!", ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="givefunds", description="Give funds to someone!")
    async def givefunds(self, interaction: discord.Interaction, user: discord.Member, amount: int) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message('They do not have a freelancer profile set!', ephemeral=True)
        else:
            await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount, user.id))
            await interaction.response.send_message(f"They were given ${amount:.2f}!", ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="balance", description="Displays your current balance!")
    async def balance(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await db.execute('INSERT INTO freelancer VALUES (?,?,?,?,?,?,?,?,?);', (interaction.user.id, 0, 'null', 'null', 'null', 'null', 'null', 'null', 'null'))
            embed = discord.Embed(
                title="",
                color=discord.Color.from_str(embed_color))
            embed.add_field(name="Wallet", value="**$0.00**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="",
                color=discord.Color.from_str(embed_color))
            embed.add_field(name="Wallet", value=f"**${a[1]:.2f}**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="earnings", description="View your earnings from Mixelate!")
    async def earnings(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from funds WHERE member_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="You have no earnings to view!", color=discord.Color.red())
        else:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Earnings", value=f"**${a[1]:.2f}**", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="spendings", description="View your spendings to Mixelate!")
    async def spendings(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from funds WHERE member_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="You have no spendings to view!", color=discord.Color.red())
        else:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Spendings", value=f"**${a[2]:.2f}**", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="calculate", description="Calculate what you need to quote to make your desired amount!")
    async def calculate(self, interaction: discord.Interaction, amount: float) -> None:
        amount1 = amount - (amount * .15)
        amount2 = amount / 85 * amount
        
        embed = discord.Embed(
            title="Freelancer Cut: 85%",
            description=f"""
If you charge **${amount:.2f}**, you will get **${amount1:.2f}**!
To get **${amount:.2f}**, you need to charge **${amount2:.2f}**!
""",
            color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, ephemeral=True)

class WalletWalletCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="wallet", description="Opens the Wallet GUI!")
    async def walletwallet(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            color=discord.Color.from_str(embed_color))
        embed.set_author(name=f"{interaction.user.name}'s Wallet", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed, view=Wallet(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(WalletCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(WalletWalletCog(bot))