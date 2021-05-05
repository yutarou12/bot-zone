from discord.ext import commands


class Join(commands.Cog):
    """入室時"""
    def __init__(self, bot):
        self.bot = bot
        self.ch_id = int(self.bot.config['Zone']['welcome_channel_id'])
        self.role_member_id = int(self.bot.config['Zone']['role_member_id'])
        self.role_bot_id = int(self.bot.config['Zone']['role_bot_id'])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel = guild.get_channel(self.ch_id)
        role_member = guild.get_role(self.role_member_id)
        role_bot = guild.get_role(self.role_bot_id)
        if channel:
            await channel.send(f'📥Join `{member}` が入室しました')
            if member.bot:
                if role_member:
                    await member.add_roles(role_bot)
            else:
                await member.add_roles(role_member)


def setup(bot):
    bot.add_cog(Join(bot))
