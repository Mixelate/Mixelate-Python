import discord
import aiosqlite
import paypalrestsdk
import datetime as DT
import yaml
import pytz
import re
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from typing import Optional

from buttons.freelancer.freelancersystem import FreelancerSystem
from buttons.commissions.commissioncomplete import TipLink
from buttons.commissions.commissioncomplete import ReviewSystem
from buttons.tickets.ticket import CommissionTicket, ApplicationTicket, SupportTicket
from src.tickets.createinvoice import createinvoice

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
client_role_id = data["Roles"]["CLIENT_ROLE_ID"]
support_specialist_role_id = data["Roles"]["SUPPORT_SPECIALIST_ROLE_ID"]
warranty_period_hours = data["General"]["WARRANTY_PERIOD_HOURS"]
transcripts_channel_id = data["Tickets"]["TRANSCRIPTS_CHANNEL_ID"]
staff_claim_ticket_channel_id = data["Tickets"]["STAFF_CLAIM_TICKET_CHANNEL_ID"]
freelancer_commission_channel_id = data["Tickets"]["FREELANCER_COMMISSION_CHANNEL_ID"]
ticket_new_price_command = data["Commands"]["TICKET_NEW_PRICE_COMMAND"]
ticket_begin_command = data["Commands"]["TICKET_BEGIN_COMMAND"]
fees_percent = data["General"]["FEES"]
x = fees_percent.replace("%", "")
y = int(x)
fee_amount = y * 0.01

paypal_client_id = data["PayPal"]["PAYPAL_CLIENT_ID"]
paypal_client_secret = data["PayPal"]["PAYPAL_CLIENT_SECRET"]

my_api = paypalrestsdk.Api({
  'mode': 'live',
  'client_id': paypal_client_id,
  'client_secret': paypal_client_secret})

class Link(discord.ui.View):
    def __init__(self, id):
        super().__init__()
        id = id
        url = f'https://www.paypal.com/invoice/s/pay/{id}'
        self.add_item(discord.ui.Button(emoji='<:paypal:1001287990464749619>', label='Pay', url=url))

class TicketCog(commands.GroupCog, name="ticket"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__() 

    def cog_load(self):
        self.paypalLoop.start()
        self.closeLoop.start()

    @tasks.loop(seconds = 5)
    async def paypalLoop(self):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * from invoices')
        a = await cursor.fetchall()
        if a is None:
            pass
        else:
            for rows in a:
                if rows[6] == "PAID":
                    continue
                else:
                    channel = self.bot.get_channel(rows[0])
                    payment = paypalrestsdk.Invoice.find(f"{rows[2]}", api=my_api)
                    x = payment['status']
                    x = "PAID"
                    if x == "PAID":
                        cursor2 = await db.execute('SELECT * FROM invoices WHERE channel_id=?', (rows[0], ))
                        b = await cursor2.fetchone()
                        payment_message = channel.get_partial_message(rows[1])
                        await db.execute('UPDATE invoices SET status=? WHERE pay_message_id=?', ('PAID', payment_message.id))
                        embed = discord.Embed(
                            title="Checkout",
                            description=
                            f"```Status: PAID \nSubtotal: ${rows[3]:.2f} \nFees ({fees_percent}): ${rows[4]:.2f} \nTotal: ${rows[5]:.2f}```",
                            color=discord.Color.from_str(embed_color))
                        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1034883707875639317/1.png")
                        await payment_message.edit(embed=embed)
                        cursor3 = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (channel.id, ))
                        c = await cursor3.fetchone()
                        msg = [message async for message in channel.history(oldest_first=True, limit=1)]
                        y = msg[0].mentions[0]
                        cursor4 = await db.execute('SELECT * FROM funds WHERE member_id=?', (y.id, ))
                        d = await cursor4.fetchone()
                        if d is None:
                            await db.execute('INSERT INTO funds VALUES (?,?,?,?,?);', (y.id, 0, b[5], 0, 1))
                        else:
                            await db.execute('UPDATE funds SET spendings=spendings+? WHERE member_id=?', (b[5], y.id))
                            await db.execute('UPDATE funds SET commissions_paid=commissions_paid+? WHERE member_id=?', (1, y.id))
                        amount = b[5] * .15 * .10
                        amount2 = b[5] - amount
                        await db.execute('UPDATE funds SET earnings=earnings+? WHERE member_id=?', (amount2, 398280171578458122))
                        await db.execute('UPDATE funds SET spendings=spendings+? WHERE member_id=?', (b[5], 398280171578458122))
                        embed = discord.Embed(description=f"The invoice has been marked as paid. <@{c[3]}> will now start the work and provide updates as progres is made!", color=discord.Color.from_str(embed_color))
                        await channel.send(content=f"{y.mention} | <@{c[3]}>", embed=embed)
                    if x == "UNPAID":
                        continue
        await db.commit()
        await db.close()

    @paypalLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()    

    @tasks.loop(seconds = 5)
    async def closeLoop(self):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM close')
        a = await cursor.fetchall()
        for row in a:
            if row[1] <= DT.datetime.now().timestamp():
                channel = self.bot.get_channel(row[0])
                try:
                    await db.execute('DELETE FROM close WHERE channel_id=?', (channel.id, ))
                except:
                    pass
                if "order" in channel.name:
                    try:
                        cursor = await db.execute('SELECT freelancer_message_id FROM commissions WHERE channel_id=?', (channel.id, ))
                        rows = await cursor.fetchone()
                        freelancer_channel = channel.guild.get_channel(freelancer_commission_channel_id)
                        freelancer_message = freelancer_channel.get_partial_message(rows[0])
                        await freelancer_message.delete()
                    except:
                        pass
                    try:
                        cursor = await db.execute('SELECT claim_id FROM commissions WHERE channel_id=?', (channel.id, ))
                        rows = await cursor.fetchone()
                        staff_claim_channel = channel.guild.get_channel(staff_claim_ticket_channel_id)
                        claim_message = staff_claim_channel.get_partial_message(rows[0])
                        await claim_message.delete()
                    except:
                        pass
                    try:
                        await db.execute('DELETE FROM quotes WHERE commissions_channel=?', (channel.id, ))
                    except:
                        pass
                    try:
                        await db.execute('DELETE FROM questions WHERE commissions_channel=?', (channel.id, ))
                    except:
                        pass
                    try:
                        await db.execute('DELETE FROM invoices WHERE channel_id=?', (channel.id, ))
                    except:
                        pass
                    try:
                        await db.execute('DELETE FROM commissions WHERE channel_id=?', (channel.id, ))
                    except:
                        pass
                if "apply" in channel.name:
                    try:
                        cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (channel.id, ))
                        a = await cursor.fetchone()
                        staff_claim_channel = channel.guild.get_channel(staff_claim_ticket_channel_id)
                        claim_message = staff_claim_channel.get_partial_message(a[3])
                        await claim_message.delete()
                    except:
                        pass
                    try:
                        await db.execute('DELETE FROM applications WHERE channel_id=?', (channel.id, ))
                    except:
                        pass
                else:
                    pass
                with open("transcripts.html", "w", encoding="utf-8") as file:
                    msg = [message async for message in channel.history(oldest_first=True, limit=1)]
                    firstmessagetime = msg[0].created_at.strftime("%m/%d/%y, %I:%M %p")
                    y = msg[0].mentions[0]
                    file.write(f"""<information> \nTicket Creator: {y} \nCreated At: {firstmessagetime} \nTicket Name: {channel} \n</information>
    <!DOCTYPE html><html><head><title>Ticket Transcript</title><meta name='viewport' content='width=device-width, initial-scale=1.0'><meta charset='UTF-8'><link href='https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap' rel='stylesheet'></head><body><style>information {{display: none;}} body {{background-color: #181d23;color: white;font-family: 'Open-Sans', sans-serif;margin: 50px;}}.ticket-header h2 {{font-weight: 400;text-transform: capitalize;margin-bottom: 0;color: #fff;}}.ticket-header p {{font-size: 14px;}}.ticket-header .children .item {{margin-right: 25px;display: flex;align-items: center;}}.ticket-header .children {{display: flex;}}.ticket-header .children .item a {{margin-right: 7px;padding: 5px 10px;padding-top: 6px;background-color: #3c434b;border-radius: 3px;font-size: 12px;}}.messages {{margin-top: 30px;display: flex;flex-direction: column;}}.messages .item {{display: flex;margin-bottom: 20px;}}.messages .item .left img {{border-radius: 100%;height: 50px;}}.messages .item .left {{margin-right: 20px;}}.messages .item .right a:nth-child(1) {{font-weight: 400;margin: 0 15px 0 0;font-size: 19px;color: #fff;}}.messages .item .right a:nth-child(2) {{text-transform: capitalize;color: #ffffff;font-size: 12px;}}.messages .item .right div {{display: flex;align-items: center;margin-top: 5px;}}.messages .item .right p {{margin: 0;white-space: normal;line-height: 2;color: #fff;font-size: 15px;}}.messages .item .right p {{max-width: 700px;margin-top: 10px;}}.messages .item {{margin-bottom: 31px;}}@media  only screen and (max-width: 600px) {{body {{margin: 0px;padding: 25px;width: calc(100% - 50px);}}.ticket-header h2 {{margin-top: 0px;}}.ticket-header .children {{display: flex;flex-wrap: wrap;}}</style><div class='ticket-header'><h2>{channel} Transcript</h2><div class='children'><div class='item'><a>CREATED</a><p>{firstmessagetime} GMT</p></div><div class='item'><a>USER</a><p>{y}</p></div></div></div><div class='messages'><div class='item'><div class='left'><img src='{channel.guild.icon}'> </div><div class='right'><div><a>{channel.guild.name}</a><a></a></div><p>Transcript File For {channel.guild.name}</p></div></div>
    """)
                    async for message in channel.history(limit=None, oldest_first=True):
                        msgtime = message.created_at.strftime("%m/%d/%y, %I:%M %p")
                        file.write(f"""<div class='item'><div class='left'><img src='{message.author.display_avatar.url}'> </div><div class='right'><div><a>{message.author}</a><a>{msgtime} GMT</a></div><p>{message.content}</p></div></div>""")
                    file.write(f"""
    <div class='item'><div class='left'><p>If a message is from a bot, and appears empty, its because the bot sent a message with no text, only an embed.</p></div></div>
    </div></body></html>
    """)
                with open("transcripts.html", "rb") as file:
                    msg = [message async for message in channel.history(oldest_first=True, limit=1)]
                    y = msg[0].mentions[0]
                    transcripts = channel.guild.get_channel(transcripts_channel_id)
                    msg = await discord.utils.get(channel.history(oldest_first=True, limit=1))
                    time = pytz.timezone('America/Tijuana')
                    created_at = msg.created_at
                    now = datetime.now(time)
                    maths = now - created_at
                    seconds = maths.total_seconds()
                    math = round(seconds)
                    embed = discord.Embed(
                        title=f"Ticket Closed!",
                        description=f"├ **Channel Name:** {channel.name} \n├ **Opened By:** {y.mention} \n├ **Opened ID:** {y.id} \n└ **Time Opened:** {math} Seconds",
                    color=discord.Color.from_str(embed_color))
                    await transcripts.send(embed=embed)
                    await transcripts.send(file=discord.File(file, f"{channel.name}.html"))
                try:
                    with open("transcripts.html", "rb") as file:
                        embed = discord.Embed(
                            title=f"Ticket Closed!",
                            description=f"├ **Channel Name:** {channel.name} \n└ **Time Opened:** {math} Seconds",
                        color=discord.Color.from_str(embed_color))
                        embed.set_footer(text="You can view the transcript below.")
                        await y.send(embed=embed)
                        await y.send(file=discord.File(file, f"{channel.name}.html"))
                except:
                    pass
                await channel.delete()
                await db.execute('DELETE FROM close WHERE channel_id=?', (row[0], ))
        await db.commit()
        await db.close()

    @closeLoop.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()    

    @app_commands.command(name="leave", description="Leaves the ticket!")
    async def leave(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            await interaction.response.send_message("This is not a commission channel!", ephemeral=True)
        else:
            if a[3] == interaction.user.id:
                embed = discord.Embed(description="Successfully left the ticket.", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await db.execute('UPDATE commissions SET freelancer_id=? WHERE channel_id=?', ('null', interaction.channel.id))
                await interaction.channel.set_permissions(interaction.user,
                    send_messages=False,
                    read_messages=False,
                    add_reactions=False,
                    embed_links=False,
                    read_message_history=False,
                    external_emojis=False,
                    use_application_commands=False)
            else:
                await interaction.response.send_message("You are not the freelancer for this commission!", ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="repost", description="Reposts the ticket!")
    async def repost(self, interaction: discord.Interaction) -> None:
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
                commissions_channel = interaction.guild.get_channel(freelancer_commission_channel_id)
                if a[3] != 'null':
                    freelancer = interaction.client.get_user(a[3])
                    await interaction.channel.set_permissions(freelancer,
                        send_messages=False,
                        read_messages=False,
                        add_reactions=False,
                        embed_links=False,
                        read_message_history=False,
                        external_emojis=False,
                        use_application_commands=False)
                if a[2] != 'null':
                    freelancer_message = commissions_channel.get_partial_message(a[2])
                    await freelancer_message.delete()
                embed = discord.Embed(title="New Commission",
                    description=f"""
**__Budget__**
{a[7]}

**__Deadline__**
{a[8]}

**__Project Description__**
{a[9]}
""",
                    color=discord.Color.from_str(embed_color))
                embed.set_footer(text="Mixelate", icon_url=interaction.guild.icon.url)
                embed.timestamp = datetime.now()
                role = interaction.guild.get_role(a[1])
                c = await commissions_channel.send(content=f'{role.mention}', embed=embed, view=FreelancerSystem())
                await db.execute('UPDATE commissions SET freelancer_message_id=? WHERE channel_id=?', (c.id, interaction.channel.id))
                await db.execute('UPDATE commissions SET freelancer_id=? WHERE channel_id=?', ('null', interaction.channel.id))
                embed = discord.Embed(description="The commission has successfully been reposted!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="addcharge", description="Creates an additional invoice!")
    @app_commands.describe(amount="How much would you like to add?")
    async def addcharge(self, interaction: discord.Interaction, amount: float) -> None:
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
                cursor2 = await db.execute('SELECT * FROM invoices WHERE channel_id=?', (interaction.channel.id, ))
                b = await cursor2.fetchone()
                if b is None:
                    embed = discord.Embed(description=f"The first invoice has not been created yet! Please use the {ticket_new_price_command} and {ticket_begin_command} commands!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    if b[6] != "PAID":
                        embed = discord.Embed(description="An invoice has not been paid. Please make sure it is paid before creating an additional invoice!", color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
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
                        await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()


    @app_commands.command(name="newprice", description="Sets the new price of the commission!")
    @app_commands.describe(amount="How much would you like to set the price to?")
    async def newprice(self, interaction: discord.Interaction, amount: float) -> None:
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
                    embed = discord.Embed(description=f"There has already been a price set for this commission. Please use the {ticket_new_price_command} command to update the price!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await db.execute('UPDATE commissions SET amount=? WHERE channel_id=?', (amount, interaction.channel.id))
                    embed = discord.Embed(description=f"{interaction.user.mention} has set the price to **${amount:.2f}**!", color=discord.Color.from_str(embed_color))
                    await interaction.channel.send(embed=embed)
                    embed = discord.Embed(description=f"The price has been set to **${amount:.2f}**!", color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="begin", description="Starts the commission!")
    async def begin(self, interaction: discord.Interaction) -> None:
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
                if a[3] == 'null':
                    embed = discord.Embed(description="There is no freelancer set for this commission!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    if a[4] == 'null':
                        embed = discord.Embed(description="There is no price set for this commission!", color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        cursor2 = await db.execute('SELECT * FROM invoices WHERE channel_id=?', (interaction.channel.id, ))
                        b = await cursor2.fetchone()
                        if b != None:
                            embed = discord.Embed(description="There has already been an invoice generated for this commission!", color=discord.Color.red())
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        else:
                            fees = a[4] * fee_amount
                            total = a[4] + fees
                            id = await createinvoice(total, a[0])
                            embed = discord.Embed(
                                title="Checkout",
                                description=
                                f"```STATUS: UNPAID \nSubtotal: ${a[4]:.2f} \nFees ({fees_percent}): ${fees:.2f} \nTotal: ${total:.2f}```",
                                color=discord.Color.from_str(embed_color))
                            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1032078238706577458/1034883707875639317/1.png")
                            x = await interaction.channel.send(embed=embed, view=Link(id))
                            await db.execute('INSERT INTO invoices VALUES (?,?,?,?,?,?,?);', (a[0], x.id, id, a[4], fees, total, 'UNPAID'))
                            embed = discord.Embed(description="The commission has begun.", color=discord.Color.from_str(embed_color))
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
                    embed = discord.Embed(description=f"There has been no price set for this commission! Please use the {ticket_new_price_command} command to set a price!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    if a[3] == 'null':
                        embed = discord.Embed(description="There is no freelancer set to this commission!", color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        cursor2 = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (a[3], ))
                        b = await cursor2.fetchone()
                        if b is None:
                            embed = discord.Embed(description=f"Failed to complete the commission! <@{a[3]} does not have a freelancer profile setup.", color=discord.Color.red())
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                        else:
                            cursor3 = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (a[6], ))
                            c = await cursor3.fetchone()
                            if c is None:
                                embed = discord.Embed(description=f"Failed to complete the commission! You do not have a freelancer profile setup.", color=discord.Color.red())
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                            else:
                                amount = a[4] - (a[4] * .15)
                                amount2 = a[4] * .15 * .10
                                amount3 = a[4] * .15 * .20
                                await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount, a[3]))
                                await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount2, interaction.user.id))
                                cursor4 = await db.execute('SELECT * FROM funds WHERE member_id=?', (a[3],))
                                d = await cursor4.fetchone()
                                if d is None:
                                    await db.execute('INSERT INTO funds VALUES (?,?,?,?,?);', (a[3], amount, 0, 1, 0))
                                else:
                                    await db.execute('UPDATE funds SET commissions_completed=commissions_completed+? WHERE member_id=?', (1, a[3]))
                                    await db.execute('UPDATE funds SET earnings=earnings+? WHERE member_id=?', (amount, a[3]))
                                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                                y = msg[0].mentions[0]
                                cursor5 = await db.execute('SELECT * FROM storedreferrals WHERE member_id=?', (y.id,))
                                e = await cursor5.fetchone()
                                if e is None:
                                    pass
                                else:
                                    referralcreator = interaction.guild.get_member(e[0])
                                    await db.execute('UPDATE referrals SET earned=earned+? WHERE member_id=?', (amount3, referralcreator.id))
                                    await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount3, referralcreator.id))
                                    embed = discord.Embed(title="Referrals", description=f"You've earned **${amount3:.2f}** from your referrals!", color=discord.Color.from_str(embed_color))
                                    await referralcreator.send(embed=embed)
                                embed = discord.Embed(title="Commission Complete",
                                    description=f"""
{interaction.user.mention} has marked this commission as completed.

Once the final product is sent, you have up to {warranty_period_hours} hours to receive a partial refund.

This ticket will automatically close in 48 hours.
""",
                                color=discord.Color.from_str(embed_color))
                                freelancer = interaction.guild.get_member(a[3])
                                embed.set_footer(text=f"${amount:.2f} has been added to {freelancer}'s account.")
                                await interaction.channel.send(embed=embed)
                                embed = discord.Embed(description=f"Please leave a rating for {freelancer.mention}!", color=discord.Color.from_str(embed_color))
                                embed.set_footer(text="Note: Reviews are publicly displayed!")
                                await interaction.channel.send(embed=embed, view=ReviewSystem())
                                if b[8] != 'null':
                                    embed = discord.Embed(description=f"If you would like to leave a tip for {freelancer.mention}, you may do so below.", color=discord.Color.from_str(embed_color))
                                    embed.set_footer(text="Note: 100% of the tip goes directly to the freelancer!")
                                    tiplink = b[8]
                                    await interaction.channel.send(embed=embed, view=TipLink(tiplink))
                                else:
                                    pass
                                await db.execute('UPDATE commissions SET amount=? WHERE channel_id=?', ('null', interaction.channel.id))
                                x = datetime.now() + timedelta(hours=48)
                                timestamp = x.timestamp()
                                ts = int(timestamp)
                                tsp = int(ts)
                                await db.execute('INSERT INTO close VALUES (?,?);', (interaction.channel.id, tsp))
                                client = interaction.guild.get_role(client_role_id)
                                try:
                                    await y.add_roles(client)
                                except:
                                    pass
                                embed = discord.Embed(description=f"The commission has been marked as complete! \n \nYou recieved **${amount2:.2f}**!", color=discord.Color.from_str(embed_color))
                                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="invite", description="Invite a user to the ticket!")
    @app_commands.describe(member="Who would you like to invite to the ticket?")
    async def invite(self, interaction: discord.Interaction, member: discord.Member) -> None:
        valid_things = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_things):
            await interaction.channel.set_permissions(member,
                send_messages=True,
                read_messages=True,
                add_reactions=True,
                embed_links=True,
                read_message_history=True,
                external_emojis=True,
                use_application_commands=True)
            embed = discord.Embed(description=f"{member.mention} has joined the ticket!", color=discord.Color.from_str(embed_color))
            await interaction.channel.send(content=member.mention, embed=embed)
            embed = discord.Embed(description="They've successfully been invited to the ticket!", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This is not a ticket channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="dismiss", description="Dismisses a user from the ticket!")
    @app_commands.describe(member="Who would you like to dismiss from the ticket?")
    async def dismiss(self, interaction: discord.Interaction, member: discord.Member) -> None:
        valid_things = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_things):
            await interaction.channel.set_permissions(member,
                send_messages=False,
                read_messages=False,
                add_reactions=False,
                embed_links=False,
                read_message_history=False,
                external_emojis=False,
                use_application_commands=False)
            embed = discord.Embed(description=f"{member.mention} has been dismissed from ticket!", color=discord.Color.from_str(embed_color))
            await interaction.channel.send(embed=embed)
            embed = discord.Embed(description="They've successfully been dismissed from the ticket!", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description="This is not a ticket channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="transcript", description="Generates a ticket transcript!")
    async def transcript(self, interaction: discord.Interaction) -> None:
        valid_things = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_things):
            with open("transcripts.html", "w", encoding="utf-8") as file:
                msg = [message async for message in interaction.channel.history(oldest_first=True, limit=1)]
                firstmessagetime = msg[0].created_at.strftime("%m/%d/%y, %I:%M %p")
                y = msg[0].mentions[0]
                file.write(f"""<information> \nTicket Creator: {y} \nCreated At: {firstmessagetime} \nTicket Name: {interaction.channel} \n</information>
    <!DOCTYPE html><html><head><title>Ticket Transcript</title><meta name='viewport' content='width=device-width, initial-scale=1.0'><meta charset='UTF-8'><link href='https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap' rel='stylesheet'></head><body><style>information {{display: none;}} body {{background-color: #181d23;color: white;font-family: 'Open-Sans', sans-serif;margin: 50px;}}.ticket-header h2 {{font-weight: 400;text-transform: capitalize;margin-bottom: 0;color: #fff;}}.ticket-header p {{font-size: 14px;}}.ticket-header .children .item {{margin-right: 25px;display: flex;align-items: center;}}.ticket-header .children {{display: flex;}}.ticket-header .children .item a {{margin-right: 7px;padding: 5px 10px;padding-top: 6px;background-color: #3c434b;border-radius: 3px;font-size: 12px;}}.messages {{margin-top: 30px;display: flex;flex-direction: column;}}.messages .item {{display: flex;margin-bottom: 20px;}}.messages .item .left img {{border-radius: 100%;height: 50px;}}.messages .item .left {{margin-right: 20px;}}.messages .item .right a:nth-child(1) {{font-weight: 400;margin: 0 15px 0 0;font-size: 19px;color: #fff;}}.messages .item .right a:nth-child(2) {{text-transform: capitalize;color: #ffffff;font-size: 12px;}}.messages .item .right div {{display: flex;align-items: center;margin-top: 5px;}}.messages .item .right p {{margin: 0;white-space: normal;line-height: 2;color: #fff;font-size: 15px;}}.messages .item .right p {{max-width: 700px;margin-top: 10px;}}.messages .item {{margin-bottom: 31px;}}@media  only screen and (max-width: 600px) {{body {{margin: 0px;padding: 25px;width: calc(100% - 50px);}}.ticket-header h2 {{margin-top: 0px;}}.ticket-header .children {{display: flex;flex-wrap: wrap;}}</style><div class='ticket-header'><h2>{interaction.channel} Transcript</h2><div class='children'><div class='item'><a>CREATED</a><p>{firstmessagetime} GMT</p></div><div class='item'><a>USER</a><p>{y}</p></div></div></div><div class='messages'><div class='item'><div class='left'><img src='{interaction.guild.icon}'> </div><div class='right'><div><a>{interaction.guild.name}</a><a></a></div><p>Transcript File For {interaction.guild.name}</p></div></div>
    """)
                async for message in interaction.channel.history(limit=None, oldest_first=True):
                    msgtime = message.created_at.strftime("%m/%d/%y, %I:%M %p")
                    file.write(f"""<div class='item'><div class='left'><img src='{message.author.display_avatar.url}'> </div><div class='right'><div><a>{message.author}</a><a>{msgtime} GMT</a></div><p>{message.content}</p></div></div>""")
                file.write(f"""
    <div class='item'><div class='left'><p>If a message is from a bot, and appears empty, its because the bot sent a message with no text, only an embed.</p></div></div>
    </div></body></html>
    """)
            with open("transcripts.html", "rb") as file:
                embed = discord.Embed(description="The transcript can be found below!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await interaction.channel.send(file=discord.File(file, f"{interaction.channel.name}.html"))
        else:
            embed = discord.Embed(description="This is not a ticket channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="close", description="Closes the ticket in the specified time!")
    @app_commands.describe(time="When should the ticket close? Ex: 15m")
    async def close(self, interaction: discord.Interaction, time: Optional[str]) -> None:
        valid_things = ("order", "apply", "support")
        if any(thing in interaction.channel.name for thing in valid_things):
            db = await aiosqlite.connect('database.db')
            cursor = await db.execute('SELECT * FROM close WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a is None:
                if time != None:
                    try:
                        time_list = re.split('(\d+)',time)
                        if time_list[2] == "s":
                            time_in_s = int(time_list[1])
                        if time_list[2] == "m":
                            time_in_s = int(time_list[1]) * 60
                        if time_list[2] == "h":
                            time_in_s = int(time_list[1]) * 60 * 60
                        if time_list[2] == "d":
                            time_in_s = int(time_list[1]) * 60 * 60 * 24
                        x = datetime.now() + timedelta(seconds=time_in_s)
                        timestamp = x.timestamp()
                        ts = int(timestamp)
                        tsp = int(ts)
                        await db.execute('INSERT INTO close VALUES (?,?);', (interaction.channel.id, tsp))
                        embed = discord.Embed(description=f"The ticket has been scheduled to close at <t:{tsp}:F>!", color=discord.Color.from_str(embed_color))
                        await interaction.channel.send(embed=embed)
                        embed = discord.Embed(description=f"You've scheduled for the ticket to close at <t:{tsp}:F>.", color=discord.Color.from_str(embed_color))
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                    except:
                        embed = discord.Embed(description=f"There was an error with {time}! Please make sure the format looks like `15m`!", color=discord.Color.red())
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    x = datetime.now() + timedelta(seconds=1)
                    timestamp = x.timestamp()
                    ts = int(timestamp)
                    tsp = int(ts)
                    await db.execute('INSERT INTO close VALUES (?,?);', (interaction.channel.id, tsp))
                    embed = discord.Embed(description="Closing...", color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(description=f"This ticket has already been scheduled to close at <t:{a[1]}:F>!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            await db.commit()
            await db.close()
        else:
            embed = discord.Embed(description="This is not a ticket channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="tip", description="Tip the freelancer!")
    async def tip(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if a[3] != 'null':
                cursor2 = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (a[3], ))
                b = await cursor2.fetchone()
                if b[8] != 'null':
                    embed = discord.Embed(title="Freelancer Tip", description=f"<@{a[3]}>'s Tip Link is set to **{b[8]}**!", color=discord.Color.from_str(embed_color))
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(description=f"<@{a[3]}> does not have a Tip Link set!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(description="There hasn't been a freelancer set to this commission!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.close()

    @app_commands.command(name="stopclose", description="Stops the ticket close timer!")
    async def stopclose(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM close WHERE channel_id=?', (interaction.channel.id, ))
        a = await cursor.fetchone()
        if a is None:
            embed = discord.Embed(description="This channel does not have a ticket close timer active!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await db.execute('DELETE FROM close WHERE channel_id=?', (interaction.channel.id, ))
            embed = discord.Embed(description="The ticket close timer has been removed.", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

class TicketTicketCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ticket", description="Opens the Ticket GUI!")
    async def ticketticket(self, interaction: discord.Interaction) -> None:
        db = await aiosqlite.connect('database.db')

        if "order" in interaction.channel.name:
            cursor = await db.execute('SELECT * FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(description="This is not a commission channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                view = CommissionTicket(self.bot)
                if interaction.user.id != a[3]:
                    view.leave.disabled = True
                if interaction.user.id != a[6]:
                    view.repost.disabled = True
                    view.addcharge.disabled = True
                    view.invite.disabled = True
                    view.transcript.disabled = True
                    view.close.disabled = True
                embed = discord.Embed(description="Select what you would like to do!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                await db.close()
                return

        if "apply" in interaction.channel.name:
            cursor = await db.execute('SELECT * FROM applications WHERE channel_id=?', (interaction.channel.id, ))
            a = await cursor.fetchone()
            if a is None:
                embed = discord.Embed(description="This is not a application channel!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                view = ApplicationTicket(self.bot)
                support_specialist = interaction.guild.get_role(support_specialist_role_id)
                if support_specialist not in interaction.user.roles:
                    view.invite.disabled = True
                    view.transcript.disabled = True
                    view.close.disabled = True
                embed = discord.Embed(description="Select what you would like to do!", color=discord.Color.from_str(embed_color))
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                await db.close()
                return

        if "support" in interaction.channel.name:
            view = SupportTicket(self.bot)
            support_specialist = interaction.guild.get_role(support_specialist_role_id)
            if support_specialist not in interaction.user.roles:
                view.invite.disabled = True
                view.transcript.disabled = True
                view.close.disabled = True
            embed = discord.Embed(description="Select what you would like to do!", color=discord.Color.from_str(embed_color))
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            await db.close()
            return
        
        else:
            embed = discord.Embed(description="This is not a ticket channel!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TicketCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(TicketTicketCog(bot))