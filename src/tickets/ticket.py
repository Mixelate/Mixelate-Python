import discord
import aiosqlite
import yaml
from discord import app_commands
from discord.ext import commands
from datetime import datetime

from src.tickets.createinvoice import createinvoice

from buttons.freelancer.freelancersystem import FreelancerSystem
from buttons.tickets.ticket import CommissionTicket

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
embed_color = data["General"]["EMBED_COLOR"]
freelancer_commission_channel_id = data["Tickets"]["FREELANCER_COMMISSION_CHANNEL_ID"]
fees_percent = data["General"]["FEES"]
x = fees_percent.replace("%", "")
y = int(x)
fee_amount = y * 0.01

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

    @app_commands.command(name="test", description="Create a test invoice!")
    async def test(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True, ephemeral=True)
        x = await createinvoice(50, interaction.channel.id)
        await interaction.followup.send(f'https://www.paypal.com/invoice/s/pay/{x}')

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
    async def addcharge(self, interaction: discord.Interaction, amount: int) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="newprice", description="Sets the new price of the commission!")
    async def newprice(self, interaction: discord.Interaction, amount: int) -> None:
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
                                f"```STATUS: UNPAID \nSubtotal: ${a[4]:.2f} \nFees {fees_percent}: ${fees:.2f} \nTotal: ${total:.2f}```",
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
                    embed = discord.Embed(description="There has been no price set for this commission! Please use the </commission setprice:1055316900407685150> command to set a price!", color=discord.Color.red())
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
                                amount3 = a[4] * .15 - amount2
                                await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount, a[3]))
                                await db.execute('UPDATE freelancer SET balance=balance+? WHERE freelancer_id=?', (amount2, interaction.user.id))
                                await db.execute('UPDATE funds SET earnings=earnings+? WHERE member_id=?', (amount3, 398280171578458122))
                                cursor4 = await db.execute('SELECT * FROM funds WHERE member_id=?', (a[3],))
                                d = await cursor4.fetchone()
                                if d is None:
                                    await db.execute('INSERT INTO funds VALUES (?,?,?,?,?);', (a[3], 0, 0, 1, 0))
                                else:
                                    await db.execute('UPDATE funds SET commissions_completed=commissions_completed+? WHERE member_id=?', (1, a[3]))
                                embed = discord.Embed(title="Commission Complete",
                                    description=f"""
This commission has been marked as complete.

**${amount:.2f}** has been added to <@{a[3]}>'s account.
""",
                                color=discord.Color.from_str(embed_color))
                                await interaction.channel.send(embed=embed)
                                await db.execute('DELETE FROM commissions WHERE channel_id=?', (interaction.channel.id, ))
                                embed = discord.Embed(description=f"The commission has been marked as complete! \n \nYou recieved **${amount2:.2f}**!", color=discord.Color.from_str(embed_color))
                                await interaction.response.send_message(embed=embed, ephemeral=True)
        await db.commit()
        await db.close()

    @app_commands.command(name="invite", description="Invite a user to the ticket!")
    @app_commands.describe(member="Who would you like to invite to the ticket?")
    async def invite(self, interaction: discord.Interaction, member: discord.Member) -> None:
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

    @app_commands.command(name="dismiss", description="Dismisses a user from the ticket!")
    @app_commands.describe(member="Who would you like to dismiss from the ticket?")
    async def dismiss(self, interaction: discord.Interaction, member: discord.Member) -> None:
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

    @app_commands.command(name="transcript", description="Generates a ticket transcript!")
    async def transcript(self, interaction: discord.Interaction) -> None:
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

    @app_commands.command(name="close", description="Closes the ticket in the specified time!")
    async def close(self, interaction: discord.Interaction, time: str) -> None:
        await interaction.response.send_message('test', ephemeral=True)

    @app_commands.command(name="review", description="Review the freelancer!")
    async def review(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message('test', ephemeral=True)

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
        if "application" in interaction.channel.name:
            await interaction.response.send_message("Coming soon...", ephemeral=True)
            await db.close()
            return
        if "support" in interaction.channel.name:
            await interaction.response.send_message("Coming soon...", ephemeral=True)
            await db.close()
            return
        embed = discord.Embed(description="Select what you would like to do!", color=discord.Color.from_str(embed_color))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await db.close()

async def setup(bot):
    await bot.add_cog(TicketCog(bot), guilds=[discord.Object(id=guild_id)])
    await bot.add_cog(TicketTicketCog(bot))