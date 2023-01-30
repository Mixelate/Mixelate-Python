import discord
import aiosqlite
import yaml

from datetime import datetime

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]

class AnswerQuestion(discord.ui.Modal, title='Respond to a Question'):

    def __init__(self, pp, dd):
        super().__init__()
        self.pp = pp
        self.dd = dd

    answer = discord.ui.TextInput(
        label='Response',
        placeholder='What is your response?',
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT * FROM questions WHERE question_message_id=?', (interaction.message.id, ))
        rows = await cursor.fetchone()
        try:
            freelancer = interaction.client.get_user(rows[1])
            embed = discord.Embed(title="New Response",
                description=f"Your question for {interaction.user.mention}'s project has been answered! \n\n**Question**: {rows[3]} \n \n**Response**: {self.answer.value}",
                color=discord.Color.from_str(embed_color))
            embed.set_footer(text=interaction.user, icon_url=interaction.user.display_avatar.url)
            embed.timestamp = datetime.now()
            await freelancer.send(embed=embed)
            for item in self.pp:
                item.disabled = True
            channel = interaction.guild.get_channel(rows[0])
            await interaction.message.edit(view=self.dd)
            question = channel.get_partial_message(rows[2])
            embed = discord.Embed(title="Answered Question",
                description=f"{freelancer.mention} has a question about your project! \n\n**Question**: {rows[3]} \n\n**Response**: {self.answer.value}",
                color=discord.Color.from_str(embed_color))
            await question.edit(embed=embed)
            await interaction.response.send_message("Successfully answered their question!", ephemeral=True)
            await db.close()
        except:
            await interaction.response.send_message("I was unable to send them a message as an error occured. \n \nThey may have DMs turned off or left the server.", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)