import discord
import aiosqlite
import yaml

from datetime import datetime

from buttons.questions.answerquestions import AnswerQuestions

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]

class Question(discord.ui.Modal, title='Ask a Question'):

    question = discord.ui.TextInput(
        label='Question',
        placeholder='What is your question?',
        max_length=2000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = await aiosqlite.connect('database.db')
        cursor = await db.execute('SELECT channel_id FROM commissions WHERE freelancer_message_id=?', (interaction.message.id, ))
        rows = await cursor.fetchone()
        commissions_channel = interaction.guild.get_channel(rows[0])
        embed = discord.Embed(title="New Question!",
                            description=f"{interaction.user.mention} has a question about your project! \n\n**{self.question.value}**",
                            color=discord.Color.from_str(embed_color))
        embed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.now()
        a = await commissions_channel.send(embed=embed, view=AnswerQuestions())
        await db.execute('INSERT INTO questions VALUES (?,?,?);', (commissions_channel.id, interaction.user.id, a.id))
        await interaction.response.send_message("You've sent a question to the commission!", ephemeral=True)
        await db.commit()
        await db.close()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)