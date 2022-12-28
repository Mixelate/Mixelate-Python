import discord
import yaml

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

embed_color = data["General"]["EMBED_COLOR"]

class WalletCalculator(discord.ui.Modal, title='Calculate Amounts'):

    amount = discord.ui.TextInput(
        label='Amount',
        placeholder='What is your desired amount?',
        max_length=10,
    )

    async def on_submit(self, interaction: discord.Interaction):
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
        amount1 = amount - (amount * .15)
        amount2 = amount / 85 * amount
        embed = discord.Embed(
            title="Freelancer Cut: 85%",
            description=f"""
If you charge **${amount:.2f}**, you will get **${amount1:.2f}**!
To get **${amount:.2f}**, you need to charge **${amount2:.2f}**!
""",
            color=discord.Color.from_str(embed_color))
        await interaction.response.edit_message(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong. Please contact <@503641822141349888> with steps on how to recreate this!', ephemeral=True)