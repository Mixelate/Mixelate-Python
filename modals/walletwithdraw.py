import discord
import aiosqlite
import yaml

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
payout_channel_id = data["Freelancer"]["PAYOUT_CHANNEL_ID"]

class RequestWalletWithdrawPayout(discord.ui.Modal, title='Requesting Your Payout!'):

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
                await interaction.response.edit_message(embed=embed)
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

class SetPayPal(discord.ui.View):
    def __init__(self, amount):
        super().__init__(timeout=None)
        self.amount = amount

    @discord.ui.button(emoji='💰', label='Set PayPal', style=discord.ButtonStyle.grey, custom_id='setpaypal:1')
    async def freelancer(self, interaction: discord.Interaction, button: discord.ui.Button):
        amount = self.amount
        await interaction.response.send_modal(RequestWalletWithdrawPayout(amount))

class WalletWithdraw(discord.ui.Modal, title='Withdraw Money!'):

    amount = discord.ui.TextInput(
        label='Amount',
        placeholder='How much would you like to withdraw?',
        max_length=10,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message("You cannot request for a payout as you do not have a profile setup!", ephemeral=True)
        else:
            if "$" in self.amount.value:
                try:
                    amount = float(self.amount.value.replace("$", ""))
                except:
                    embed = discord.Embed(
                        title="Error",
                        description=f"The value you provided is not valid. Please be sure it is a valid integer!",
                        color=discord.Color.red())
                    await interaction.response.edit_message(embed=embed)
                    return
            else:
                try:
                    amount = float(self.amount.value)
                except:
                    embed = discord.Embed(
                        title="Error",
                        description=f"The value you provided is not valid. Please be sure it is a valid integer!",
                        color=discord.Color.red())
                    await interaction.response.edit_message(embed=embed)
                    return
                if a[1] >= amount:
                    if a[7] == 'null':
                        embed = discord.Embed(
                            title="Error",
                            description=f"You must set your paypal to request for a withdrawl. Click the button below to set it!",
                            color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, view=SetPayPal(amount), ephemeral=True)
                    else:
                        embed = discord.Embed(
                            title="Withdrawl Successful",
                            description=f"""
You have successfully requested for a withdrawl of **${amount:.2f}**! You will receive a DM once it has been approved!
""",
                        color=discord.Color.from_str(embed_color))
                        await interaction.response.edit_message(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error",
                        description=f"You do not have ${amount:.2f} to withdraw!",
                        color=discord.Color.red())
                    await interaction.response.edit_message(embed=embed)

    #async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
    #    await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)