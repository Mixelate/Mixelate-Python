import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]

class CommissionCog(commands.GroupCog, name="commission"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @app_commands.command(name="setprice", description="Sets a price for the commission!")
    @app_commands.describe(amount="What do you want to set the price to?")
    async def setpprice(self, interaction: discord.Interaction, amount: float) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if interaction.user.id != a[6]:
                embed = discord.Embed(description="You are not the commission manager for this commission!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if a[4] != 'null':
                    embed = discord.Embed(description="There has already been a price set for this commission. Please use the </commission update:1055316900407685150> command to update the price!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await db.execute('UPDATE commissions SET amount=? WHERE channel_id=?', (amount, interaction.channel.id))
                    embed = discord.Embed(description=f"{interaction.user.mention} has set the price. The price was set to **${amount:.2f}**!", color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(embed=embed)
                    embed = discord.Embed(description=f"The price has been set to **${amount:.2f}**!", color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="update", description="Updates the price for the commission!")
    @app_commands.describe(amount="What do you want to update the price to?")
    async def update(self, interaction: discord.Interaction, amount: float) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if interaction.user.id != a[6]:
                embed = discord.Embed(description="You are not the commission manager for this commission!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if a[4] == 'null':
                    embed = discord.Embed(description="There hasn't been a price set! Please use the </commission setprice:1055316900407685150> command to set a price!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await db.execute('UPDATE commissions SET amount=? WHERE channel_id=?', (amount, interaction.channel.id))
                    embed = discord.Embed(description=f"{interaction.user.mention} has updated the price. The price is now **${amount:.2f}**!", color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(embed=embed)
                    embed = discord.Embed(description=f"The price has been updated to **${amount:.2f}**!", color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="complete", description="Completes a commission!")
    async def complete(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if interaction.user.id != a[6]:
                embed = discord.Embed(description="You are not the commission manager for this commission!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                if a[4] == 'null':
                    embed = discord.Embed(description="There has been no price set for this commission! Please use the </commission setprice:1055316900407685150> command to set a price!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    if a[3] == 'null':
                        embed = discord.Embed(description="There is no freelancer set to this commission!", color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (a[3], ))
                        b = await cursor.fetchone()
                        if b is None:
                            embed = discord.Embed(description=f"Failed to complete the commission! <@{a[3]} does not have a freelancer profile setup.", color=discord.Color.red())
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        else:
                            cursor2 = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (a[6], ))
                            c = await cursor2.fetchone()
                            if c is None:
                                embed = discord.Embed(description=f"Failed to complete the commission! You do not have a freelancer profile setup.", color=discord.Color.red())
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                            else:
                                amount = a[4] - (a[4] * .15)
                                await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount, a[3]))
                                embed = discord.Embed(title="Commission Complete",
                                    description=f"""
This commission has been marked as complete.

**${amount:.2f}** has been added to <@{a[3]}>'s account.
""",
                                color=discord.Color.from_str(embed_color))
                                await interaction.channel.send(embed=embed)
                                await db.execute('DELETE FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
                                embed = discord.Embed(description="The commission has been marked as complete!", color=discord.Color.from_str(embed_color))
                                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

async def setup(bot):
    await bot.add_cog(CommissionCog(bot), guilds=[discord.Object(id=guild_id)])