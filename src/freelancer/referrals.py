import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from buttons.freelancer.referrals import ReferralsButtons

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
referral_generate_command = data["Commands"]["REFERRAL_GENERATE_COMMAND"]
referral_delete_command = data["Commands"]["REFERRAL_DELETE_COMMAND"]

class ReferralsCog(commands.GroupCog, name="referrals"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals')
        a = await cursor.fetchall()
        guild = self.bot.get_guild(guild_id)
        invites = await guild.invites()
        for i in invites:
            for r in a:
                if r[1] == i.code:
                    if r[2] != i.uses:
                        await db.execute('UPDATE referrals SET uses=? WHERE invite_code=?', (i.uses, r[1]))
                        cursor2 = await db.execute('SELECT * from storedreferrals WHERE member_id=?', (member.id,))
                        b = await cursor2.fetchone()
                        if b is not None:
                            await db.execute('DELETE FROM storedreferrals WHERE member_id=?', (member.id, ))
                        await db.execute('INSERT INTO storedreferrals VALUES (?,?);', (r[0], member.id))
                        creator = guild.get_member(r[0])
                        embed = discord.Embed(title="Referral Added", description=f"{member.mention} has been joined using your referral link! \n\nYou will get 20% of 15% of their orders!", color=discord.Color.from_str(embed_color))
                        await creator.send(embed=embed)
        await db.commit()
        await db.close()

    @app_commands.command(name="earned", description="View your income from referrals!")
    async def earned(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You have not created a referral link! Use the {referral_generate_command} command to generate one!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Earned", value=f"**${a[3]:.2f}**")
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @app_commands.command(name="generate", description="Generate a referral link!")
    async def generate(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            invite = await interaction.channel.create_invite()
            await db.execute('INSERT INTO referrals VALUES (?,?,?,?);', (interaction.user.id, invite.code, 0, 0))
            embed = discord.Embed(description=f"You have successfully created a refferal link! The referral link is `{invite.code}`! \n{invite}", color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                await self.bot.fetch_invite(a[1])
                embed = discord.Embed(description=f"You already have an active referral link! You can use the {referral_delete_command} to delete it!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                await db.execute('DELETE FROM referrals WHERE invite_code=?', (a[1], ))
                invite = await interaction.channel.create_invite()
                await db.execute('INSERT INTO referrals VALUES (?,?,?,?);', (interaction.user.id, invite.code, 0, 0))
                embed = discord.Embed(description=f"Your previous referral link was invalid. The new valid referral link is `{invite.code}`! \n{invite}", color=discord.Color.from_str(embed_color))
                embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="delete", description="Deletes a referral link!")
    async def delete(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You do not have any active referral links! Use the {referral_generate_command} to generate one!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            try:
                await self.bot.delete_invite(a[1])
            except:
                pass
            await db.execute('DELETE FROM referrals WHERE invite_code=?', (a[1], ))
            embed = discord.Embed(description="You have successfully deleted your referral link!", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="active", description="Displays all active referals!")
    async def active(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You do not have an active referral link! Use the {referral_generate_command} to generate one!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description=f"Your active referral link's code is `{a[1]}` (https://discord.gg/{a[1]})", color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @app_commands.command(name="info", description="Displays your referral's information!")
    async def info(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You do not have any active referral links! Use the {referral_generate_command} to genertae one!", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Code", value=f"**{a[1]}**", inline=True)
            embed.add_field(name="Uses", value=f"**{a[2]}**", inline=True)
            embed.add_field(name="Earned", value=f"**${a[3]:.2f}**", inline=True)
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

class ReferralsReferralsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="referrals", description="Opens the Referrals GUI!")
    async def referralsreferrals(self, interaction: discord.Interaction) -> None:
        bot = self.bot
        view = ReferralsButtons(bot)
        embed = discord.Embed(description="Select what you would like to do!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReferralsCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(ReferralsReferralsCog(bot))