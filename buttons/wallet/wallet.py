import discord
import aiosqlite
import yaml
from discord.ext import commands

from modals.walletcalculator import WalletCalculator
from modals.walletwithdraw import WalletWithdraw

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
payout_channel_id = data["Freelancer"]["PAYOUT_CHANNEL_ID"]

class Wallet(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='💰', label='Earnings', style=discord.ButtonStyle.gray, custom_id='wallet:1')
    async def earnings(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('test', ephemeral=True)

    @discord.ui.button(emoji='💵', label='Balance', style=discord.ButtonStyle.gray, custom_id='wallet:2')
    async def balance(self, interaction: discord.Interaction, button: discord.ui.Button):
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
            await interaction.response.edit_message(embed=embed)
        else:
            embed = discord.Embed(
                title="",
                color=discord.Color.from_str(embed_color))
            embed.add_field(name="Wallet", value=f"**${a[1]:.2f}**", inline=True)
            embed.set_author(name=f"{interaction.user.name}'s Balance", icon_url=interaction.user.avatar.url)
            await interaction.response.edit_message(embed=embed)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='🤑', label='Withdraw', style=discord.ButtonStyle.gray, custom_id='wallet:3')
    async def withdraw(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WalletWithdraw())

    @discord.ui.button(emoji='🧮', label='Calculator', style=discord.ButtonStyle.gray, custom_id='wallet:4')
    async def calculator(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(WalletCalculator())

class WalletCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(Wallet())

async def setup(bot):
    await bot.add_cog(WalletCog(bot), guilds=[discord.Object(id=guild_id)])