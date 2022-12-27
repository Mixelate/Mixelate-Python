import discord
import aiosqlite
import yaml

from datetime import datetime

from buttons.quotes.quotes import Quotes

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]

class Quote(discord.ui.Modal, title='Give a Quote'):

    quote = discord.ui.TextInput(
        label='Quote',
        placeholder='What is your quote?',
        max_length=5,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT channel_id FROM commissions WHERE freelancer_message_id=?', (interaction.message.id, ))
        rows = await cursor.fetchone()
        cursor = await db.execute('SELECT * FROM freelancer WHERE freelancer_id=?', (interaction.user.id, ))
        a = await cursor.fetchone()
        commissions_channel = interaction.guild.get_channel(rows[0])
        if a[4] == 'null':
            portfolio = "**N/A**"
        else:
            portfolio = a[4]
        embed = discord.Embed(title="New Quote!",
                            description=f"{interaction.user.mention} offered to complete your project for **${self.quote.value}**! \n \nPortfolio: {portfolio}",
                            color=discord.Color.from_str(embed_color))
        embed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.now()
        a = await commissions_channel.send(embed=embed, view=Quotes())
        await db.execute('INSERT INTO quotes VALUES (?,?,?);', (commissions_channel.id, interaction.user.id, a.id))
        await db.commit()
        await db.close()
        await interaction.response.send_message("Your quote has been recieved!", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)