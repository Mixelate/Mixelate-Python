import discord
import aiosqlite
import datetime as DT
import yaml
from discord.ext import commands
from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
commission_manager_role_id = data["Roles"]["COMMISSION_MANAGER_ROLE_ID"]
reviews_channel_id = data["Tickets"]["REVIEWS_CHANNEL_ID"]

class TipLink(discord.ui.View):
    def __init__(self, tiplink):
        super().__init__()
        url = tiplink
        self.add_item(discord.ui.Button(emoji='<:paypal:1001287990464749619>', label='Tip', url=url))

class ReviewOneStar(discord.ui.Modal, title='Review One Star'):

    def __init__(self, pp, dd, freelancer):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.freelancer = freelancer

        self.review = discord.ui.TextInput(
            label=f'Review for {self.freelancer}',
            placeholder=f'What is your review for {self.freelancer}?',
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )

        self.add_item(self.review)

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id,))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                for item in self.pp:
                    item.disabled = True
                await interaction.message.edit(view=self.dd)
                timestamp = int(DT.datetime.now().timestamp())
                service = interaction.guild.get_role(b[1])
                await db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?);', (self.freelancer.id, interaction.user.id, interaction.channel.id, service.id, self.review.value, 1, timestamp))
                embed = discord.Embed(title=f"New Review from {interaction.user.name}", color=discord.Color.from_str(embed_color))
                embed.add_field(name="Service Provided", value=service.mention, inline=False)
                embed.add_field(name="Freelancer", value=self.freelancer, inline=False)
                embed.add_field(name="Rating", value="⭐ (1.0)", inline=False)
                embed.add_field(name="Comment", value=self.review.value, inline=False)
                embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
                embed.timestamp = datetime.now()
                review_channel = interaction.guild.get_channel(reviews_channel_id)
                await review_channel.send(embed=embed)
                embed = discord.Embed(description=f"You have successfully posted a review for {self.freelancer.mention}!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewTwoStar(discord.ui.Modal, title='Review Two Star'):

    def __init__(self, pp, dd, freelancer):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.freelancer = freelancer

        self.review = discord.ui.TextInput(
            label=f'Review for {self.freelancer}',
            placeholder=f'What is your review for {self.freelancer}?',
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )

        self.add_item(self.review)

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id,))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                for item in self.pp:
                    item.disabled = True
                await interaction.message.edit(view=self.dd)
                timestamp = int(DT.datetime.now().timestamp())
                service = interaction.guild.get_role(b[1])
                await db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?);', (self.freelancer.id, interaction.user.id, interaction.channel.id, service.id, self.review.value, 2, timestamp))
                embed = discord.Embed(title=f"New Review from {interaction.user.name}", color=discord.Color.from_str(embed_color))
                embed.add_field(name="Service Provided", value=service.mention, inline=False)
                embed.add_field(name="Freelancer", value=self.freelancer, inline=False)
                embed.add_field(name="Rating", value="⭐⭐ (2.0)", inline=False)
                embed.add_field(name="Comment", value=self.review.value, inline=False)
                embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
                embed.timestamp = datetime.now()
                review_channel = interaction.guild.get_channel(reviews_channel_id)
                await review_channel.send(embed=embed)
                embed = discord.Embed(description=f"You have successfully posted a review for {self.freelancer.mention}!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewThreeStar(discord.ui.Modal, title='Review Three Star'):

    def __init__(self, pp, dd, freelancer):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.freelancer = freelancer

        self.review = discord.ui.TextInput(
            label=f'Review for {self.freelancer}',
            placeholder=f'What is your review for {self.freelancer}?',
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )

        self.add_item(self.review)

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id,))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                for item in self.pp:
                    item.disabled = True
                await interaction.message.edit(view=self.dd)
                timestamp = int(DT.datetime.now().timestamp())
                service = interaction.guild.get_role(b[1])
                await db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?);', (self.freelancer.id, interaction.user.id, interaction.channel.id, service.id, self.review.value, 3, timestamp))
                embed = discord.Embed(title=f"New Review from {interaction.user.name}", color=discord.Color.from_str(embed_color))
                embed.add_field(name="Service Provided", value=service.mention, inline=False)
                embed.add_field(name="Freelancer", value=self.freelancer, inline=False)
                embed.add_field(name="Rating", value="⭐⭐⭐ (3.0)", inline=False)
                embed.add_field(name="Comment", value=self.review.value, inline=False)
                embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
                embed.timestamp = datetime.now()
                review_channel = interaction.guild.get_channel(reviews_channel_id)
                await review_channel.send(embed=embed)
                embed = discord.Embed(description=f"You have successfully posted a review for {self.freelancer.mention}!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewFourStar(discord.ui.Modal, title='Review Four Star'):

    def __init__(self, pp, dd, freelancer):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.freelancer = freelancer

        self.review = discord.ui.TextInput(
            label=f'Review for {self.freelancer}',
            placeholder=f'What is your review for {self.freelancer}?',
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )

        self.add_item(self.review)

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id,))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                for item in self.pp:
                    item.disabled = True
                await interaction.message.edit(view=self.dd)
                timestamp = int(DT.datetime.now().timestamp())
                service = interaction.guild.get_role(b[1])
                await db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?);', (self.freelancer.id, interaction.user.id, interaction.channel.id, service.id, self.review.value, 4, timestamp))
                embed = discord.Embed(title=f"New Review from {interaction.user.name}", color=discord.Color.from_str(embed_color))
                embed.add_field(name="Service Provided", value=service.mention, inline=False)
                embed.add_field(name="Freelancer", value=self.freelancer, inline=False)
                embed.add_field(name="Rating", value="⭐⭐⭐⭐ (4.0)", inline=False)
                embed.add_field(name="Comment", value=self.review.value, inline=False)
                embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
                embed.timestamp = datetime.now()
                review_channel = interaction.guild.get_channel(reviews_channel_id)
                await review_channel.send(embed=embed)
                embed = discord.Embed(description=f"You have successfully posted a review for {self.freelancer.mention}!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewFiveStar(discord.ui.Modal, title='Review Five Star'):

    def __init__(self, pp, dd, freelancer):
        super().__init__()
        self.pp = pp
        self.dd = dd
        self.freelancer = freelancer

        self.review = discord.ui.TextInput(
            label=f'Review for {self.freelancer}',
            placeholder=f'What is your review for {self.freelancer}?',
            max_length=1000,
            style=discord.TextStyle.paragraph,
        )

        self.add_item(self.review)

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id,))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id,))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                for item in self.pp:
                    item.disabled = True
                await interaction.message.edit(view=self.dd)
                timestamp = int(DT.datetime.now().timestamp())
                service = interaction.guild.get_role(b[1])
                await db.execute('INSERT INTO reviews VALUES (?,?,?,?,?,?,?);', (self.freelancer.id, interaction.user.id, interaction.channel.id, service.id, self.review.value, 5, timestamp))
                embed = discord.Embed(title=f"New Review from {interaction.user.name}", color=discord.Color.from_str(embed_color))
                embed.add_field(name="Service Provided", value=service.mention, inline=False)
                embed.add_field(name="Freelancer", value=self.freelancer, inline=False)
                embed.add_field(name="Rating", value="⭐⭐⭐⭐⭐ (5.0)", inline=False)
                embed.add_field(name="Comment", value=self.review.value, inline=False)
                embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
                embed.timestamp = datetime.now()
                review_channel = interaction.guild.get_channel(reviews_channel_id)
                await review_channel.send(embed=embed)
                embed = discord.Embed(description=f"You have successfully posted a review for {self.freelancer.mention}!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)

class ReviewSystem(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='⭐', label='1', style=discord.ButtonStyle.grey, custom_id='review:1')
    async def onestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                y = msg[0].mentions[0]
                if y.id == interaction.user.id:
                    pp = self.children
                    dd = self
                    freelancer = interaction.guild.get_member(b[3])
                    await interaction.response.send_modal(ReviewOneStar(pp, dd, freelancer))
                else:
                    embed = discord.Embed(description="You cannot review this freelancer because you're not the ticket creator!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @discord.ui.button(emoji='⭐', label='2', style=discord.ButtonStyle.grey, custom_id='review:2')
    async def twostar(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                y = msg[0].mentions[0]
                if y.id == interaction.user.id:
                    pp = self.children
                    dd = self
                    freelancer = interaction.guild.get_member(b[3])
                    await interaction.response.send_modal(ReviewTwoStar(pp, dd, freelancer))
                else:
                    embed = discord.Embed(description="You cannot review this freelancer because you're not the ticket creator!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @discord.ui.button(emoji='⭐', label='3', style=discord.ButtonStyle.grey, custom_id='review:3')
    async def threestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                y = msg[0].mentions[0]
                if y.id == interaction.user.id:
                    pp = self.children
                    dd = self
                    freelancer = interaction.guild.get_member(b[3])
                    await interaction.response.send_modal(ReviewThreeStar(pp, dd, freelancer))
                else:
                    embed = discord.Embed(description="You cannot review this freelancer because you're not the ticket creator!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @discord.ui.button(emoji='⭐', label='4', style=discord.ButtonStyle.grey, custom_id='review:4')
    async def fourstar(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                y = msg[0].mentions[0]
                if y.id == interaction.user.id:
                    pp = self.children
                    dd = self
                    freelancer = interaction.guild.get_member(b[3])
                    await interaction.response.send_modal(ReviewFourStar(pp, dd, freelancer))
                else:
                    embed = discord.Embed(description="You cannot review this freelancer because you're not the ticket creator!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @discord.ui.button(emoji='⭐', label='5', style=discord.ButtonStyle.grey, custom_id='review:5')
    async def fivestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from reviews WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            cursor2 = await db.execute('SELECT * from commissions WHERE channel_id=?', (interaction.channel.id, ))
            b = await cursor2.fetchone()
            if b is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                y = msg[0].mentions[0]
                if y.id == interaction.user.id:
                    pp = self.children
                    dd = self
                    freelancer = interaction.guild.get_member(b[3])
                    await interaction.response.send_modal(ReviewFiveStar(pp, dd, freelancer))
                else:
                    embed = discord.Embed(description="You cannot review this freelancer because you're not the ticket creator!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This channel has already had a review posted!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

class CommissionCompleteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(ReviewSystem())

async def setup(bot):
    await bot.add_cog(CommissionCompleteCog(bot), guilds=[discord.Object(id=guild_id)])