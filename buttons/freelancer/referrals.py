import discord
import aiosqlite
import yaml
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
referral_generate_command = data["Commands"]["REFERRAL_GENERATE_COMMAND"]
referral_delete_command = data["Commands"]["REFERRAL_DELETE_COMMAND"]

class ReferralsButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(emoji='💰', label='Earned', style=discord.ButtonStyle.gray, custom_id='referrals_buttons:1')
    async def earned(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You do not have any active referral links! Use the {referral_generate_command} to genertae one!", color=discord.Color.from_str(embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Earned", value=f"**${a[3]:.2f}**")
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)
        await db.close()

    @discord.ui.button(emoji='👌', label='Generate', style=discord.ButtonStyle.gray, custom_id='referrals_buttons:2')
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            invite = await interaction.channel.create_invite()
            await db.execute('INSERT INTO referrals VALUES (?,?,?,?);', (interaction.user.id, invite.code, 0, 0))
            embed = discord.Embed(description=f"You have successfully created a refferal link! The referral link is `{invite.code}`! \n{invite}", color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            try:
                await self.bot.fetch_invite(a[1])
                embed = discord.Embed(description=f"You already have an active referral link! You can use the {referral_delete_command} to delete it!", color=discord.Color.red())
                await interaction.response.edit_message(embed=embed, view=None)
            except:
                await db.execute('DELETE FROM referrals WHERE invite_code=?', (a[1], ))
                invite = await interaction.channel.create_invite()
                await db.execute('INSERT INTO referrals VALUES (?,?,?,?);', (interaction.user.id, invite.code, 0, 0))
                embed = discord.Embed(description=f"Your previous referral link was invalid. The new valid referral link is `{invite.code}`! \n{invite}", color=discord.Color.from_str(embed_color))
                embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                await interaction.response.edit_message(embed=embed, view=None)
        await db.commit()
        await db.close()

    @discord.ui.button(emoji='🤝', label='Active', style=discord.ButtonStyle.gray, custom_id='referrals_buttons:3')
    async def active(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You do not have any active referral links! Use the {referral_generate_command} to genertae one!", color=discord.Color.from_str(embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(description=f"Your active referral link's code is `{a[1]}` (https://discord.gg/{a[1]})", color=discord.Color.from_str(embed_color))
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)
        await db.close()

    @discord.ui.button(emoji='🤑', label='Info', style=discord.ButtonStyle.gray, custom_id='referrals_buttons:4')
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from referrals WHERE member_id=?', (interaction.user.id,))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description=f"You do not have any active referral links! Use the {referral_generate_command} to genertae one!", color=discord.Color.from_str(embed_color))
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(color=discord.Color.from_str(embed_color))
            embed.add_field(name="Code", value=f"**{a[1]}**", inline=True)
            embed.add_field(name="Uses", value=f"**{a[2]}**", inline=True)
            embed.add_field(name="Earned", value=f"**${a[3]:.2f}**", inline=True)
            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)
        await db.close()

class ReferralsButtonsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ReferralsButtons(bot))

async def setup(bot):
    await bot.add_cog(ReferralsButtonsCog(bot), guilds=[discord.Object(id=guild_id)])