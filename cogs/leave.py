from discord.ext import commands


class Leave(commands.Cog):
    """退出時"""
    def __init__(self, bot):
        self.bot = bot
        self.ch_id = self.bot.config['Zone']['welcome_channel_id']

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        channel = guild.get_channel(self.ch_id)
        if channel:
            await channel.send(f'📤Leave `{member}` が退出しました')
