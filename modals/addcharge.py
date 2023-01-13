import discord
import aiosqlite
import yaml

from src.tickets.createinvoice import createinvoice

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]
fees_percent = data["General"]["FEES"]
ticket_new_price_command = data["Commands"]["TICKET_NEW_PRICE_COMMAND"]
ticket_begin_command = data["Commands"]["TICKET_BEGIN_COMMAND"]
x = fees_percent.replace("%", "")
y = int(x)
fee_amount = y * 0.01

class Link(discord.ui.View):
    def __init__(self, id):
        super().__init__()
        id = id
        url = f'https://www.paypal.com/invoice/s/pay/{id}'
        self.add_item(discord.ui.Button(emoji='<:paypal:1001287990464749619>', label='Pay', url=url))

class AddCharge(discord.ui.Modal, title='Adds a Charge'):

    def __init__(self):
        super().__init__()

    amount = discord.ui.TextInput(
        label='Amount',
        placeholder='How much would you like to add?',
        max_length=6,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = float(self.amount.value)
        except:
            embed = discord.Embed(description="You must provide a valid integer to add a charge!", color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)
            return
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            if interaction.user.id != a[6]:
                embed = discord.Embed(description="You are not the commission manager for this commission!", color=discord.Color.red())
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                cursor2 = await db.execute('SELECT * FROM invoices WHERE channel_id=?', (interaction.channel.id, ))
                b = await cursor2.fetchone()
                if b is None:
                    embed = discord.Embed(description=f"The first invoice has not been created yet! Please use the {ticket_new_price_command} and {ticket_begin_command} commands!", color=discord.Color.red())
                    await interaction.response.edit_message(embed=embed, view=None)
                else:
                    if b[6] != "PAID":
                        embed = discord.Embed(description="An invoice has not been paid. Please make sure it is paid before creating an additional invoice!", color=discord.Color.red())
                        await interaction.response.edit_message(embed=embed, view=None)
                    else:
                        fees = amount * fee_amount
                        total = amount + fees
                        id = await createinvoice(total, a[0])
                        embed1 = discord.Embed(description=f"{interaction.user.mention} has created an additional invoice for **${amount}**!", color=discord.Color.from_str(embed_color))
                        embed2 = discord.Embed(
                            title="Checkout",
                            description=
                            f"```STATUS: UNPAID \nSubtotal: ${amount:.2f} \nFees ({fees_percent}): ${fees:.2f} \nTotal: ${total:.2f}```",
                            color=discord.Color.from_str(embed_color))
                        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1034883707875639317/1.png")
                        await interaction.channel.send(embed=embed1)
                        x = await interaction.channel.send(embed=embed2, view=Link(id))
                        await db.execute('UPDATE commissions SET amount=amount+? WHERE channel_id=?', (amount, a[0]))
                        await db.execute('INSERT INTO invoices VALUES (?,?,?,?,?,?,?);', (a[0], x.id, id, amount, fees, total, 'UNPAID'))
                        embed = discord.Embed(description=f"You have created an additional invoice for **${amount}**!", color=discord.Color.from_str(embed_color))
                        await interaction.response.edit_message(embed=embed, view=None)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)