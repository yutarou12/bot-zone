from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx):
        await ctx.reply("フェイクだよ？")
