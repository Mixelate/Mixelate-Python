import discord
import yaml
from discord.ext import commands

from modals.answerquestion import AnswerQuestion

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

guild_id = data["General"]["GUILD_ID"]

class AnswerQuestions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='📨', label='Reply', style=discord.ButtonStyle.blurple, custom_id='questions:1')
    async def reply(self, interaction: discord.Interaction, button: discord.ui.Button):
        pp = self.children
        dd = self
        await interaction.response.send_modal(AnswerQuestion(pp, dd))

class AnswerQuestionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(AnswerQuestions())

async def setup(bot):
    await bot.add_cog(AnswerQuestionsCog(bot), guilds=[discord.Object(id=guild_id)])