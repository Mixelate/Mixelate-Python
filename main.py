import discord
import asyncio
import aiosqlite
import yaml
import sys
from discord.ext.commands import CommandNotFound
from discord.ext import commands

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]
activity = data["General"]["ACTIVITY"].lower()
doing_activity = data["General"]["DOING_ACTIVITY"]
streaming_activity_twitch_url = data["General"]["STREAMING_ACTIVITY_TWITCH_URL"]
status = data["General"]["STATUS"].lower()
token = data["General"]["TOKEN"]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if status == "online":
    _status = getattr(discord.Status, status)
elif status == "idle":
    _status = getattr(discord.Status, status)
elif status == "dnd":
    _status = getattr(discord.Status, status)
elif status == "invisible":
    _status = getattr(discord.Status, status)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Status: {bcolors.ENDC}{bcolors.OKCYAN}{status}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}online{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}idle{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}dnd{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}invisible{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 7
""")

if activity == "playing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Game(name=doing_activity)
elif activity == "watching":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.watching)
elif activity == "listening":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.listening)
elif activity == "streaming":
    if streaming_activity_twitch_url == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Streaming Activity Twitch URL: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 6
""")
    elif not "https://twitch.tv/" in streaming_activity_twitch_url:
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Streaming Activity Twitch URL: {bcolors.OKBLUE}It Must Be A Valid Twitch URL!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 6
""")
    else:
        _activity = discord.Streaming(name=doing_activity, url=streaming_activity_twitch_url)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Activity: {bcolors.ENDC}{bcolors.OKCYAN}{activity}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}playing{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}watching{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}listening{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}streaming{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 4
""")

intents = discord.Intents.all()
intents.message_content = True

initial_extensions = [
                      'buttons.applications.applicationsystem',
                      'buttons.applications.claimapplicationticket',
                      'buttons.commissions.claimcommissionticket',
                      'buttons.freelancer.freelancersystem',
                      'buttons.questions.answerquestions',
                      'buttons.quotes.quotes',
                      'buttons.tickets.ticket',
                      'buttons.tickets.ticketclose',
                      'buttons.tickets.ticketsystem',
                      'buttons.wallet.wallet',
                      'dropdowns.order.ordercreative',
                      'dropdowns.order.orderdesign',
                      'dropdowns.order.orderdevelopment',
                      'dropdowns.order.orderdropdown',
                      'dropdowns.order.ordersetups',
                      'dropdowns.order.ordervideo',
                      'dropdowns.order.orderweb',
                      'dropdowns.freelancerapplication',
                      'dropdowns.staffapplication',
                      'src.applications.applications',
                      'src.admin.admin',
                      'src.freelancer.freelancer',
                      'src.freelancer.portfolio',
                      'src.freelancer.profile',
                      'src.freelancer.referals',
                      'src.freelancer.wallet',
                      'src.general.help',
                      'src.tickets.ticket',
                      'src.utils.say',
                      'src.utils.utils'
                      ]

class TicketBotView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Test', style=discord.ButtonStyle.green, custom_id='test:1')
    async def test(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Testing the system...', ephemeral=True)

class TicketBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), owner_id=503641822141349888, intents=intents, activity=_activity, status=_status)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(TicketBotView())
            self.persistent_views_added = True

        print(f'Signed in as {self.user}')

        await self.tree.sync(guild=discord.Object(id=guild_id))
        await self.tree.sync()

    async def setup_hook(self):
        for extension in initial_extensions:
            await self.load_extension(extension)

client = TicketBot()
client.remove_command('help')

@client.command()
@commands.is_owner()
async def sqlite(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE quotes (
        commissions_channel INTEGER,
        member_id INTEGER,
        quote_message_id INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE quotes;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite2(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE commissions (
        channel_id INTEGER,
        role_id INTEGER,
        freelancer_message_id INTEGER,
        freelancer_id INTEGER,
        amount INTEGER,
        claim_id INTEGER,
        commission_manager INTEGER,
        budget INTEGER,
        deadline STRING,
        description STRING
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete2(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE commissions;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite3(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE questions (
        commissions_channel INTEGER,
        member_id INTEGER,
        question_message_id,
        question STRING
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete3(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE questions;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite4(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE freelancer (
        freelancer_id INTEGER,
        balance INTEGER,
        title STRING,
        description STRING,
        portfolio STRING,
        pronouns STRING,
        timezone STRING,
        paypal STRING,
        paypalme STRING
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete4(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE freelancer;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite5(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE applications (
        applicant_id INTEGER,
        channel_id INTEGER,
        roles STRING,
        claim_id INTEGER,
        application_reviewer INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete5(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE applications;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite6(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE invoices (
        channel_id INTEGER,
        pay_message_id INTEGER,
        invoice_id STRING,
        subtotal INTEGER,
        fees INTEGER,
        total INTEGER,
        status INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete6(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE invoices;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite7(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE tickets (
        valid_roles INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.execute('INSERT INTO tickets VALUES (?);', (1042254331510001714,))
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete7(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE tickets;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite8(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE funds (
        member_id INTEGER,
        earnings INTEGER,
        spendings INTEGER,
        commissions_completed INTEGER,
        commissions_paid INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.execute('INSERT INTO funds VALUES (?,?,?,?,?);', (398280171578458122, 0, 0, 0, 0))
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete8(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE funds;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

@client.command()
@commands.is_owner()
async def sqlite9(ctx):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute("""
   CREATE TABLE warns (
        member_id INTEGER,
        moderator INTEGER,
        reason STRING,
        time_issued INTEGER,
        case_number INTEGER
    )""")
    await cursor.close()
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await a.delete()
    await ctx.message.delete()

@client.command()
@commands.is_owner()
async def delete9(ctx):
    db = await aiosqlite.connect('database.db')
    await db.execute('DROP TABLE warns;')
    await db.commit()
    await db.close()
    a = await ctx.reply('Done!')
    await asyncio.sleep(5)
    await ctx.message.delete()
    await a.delete()

#\\\\\\\\\\\\Error Handler////////////
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

client.run(token)