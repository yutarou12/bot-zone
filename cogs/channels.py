import discord
from discord.ext import commands


class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_bot_id = int(self.bot.config['Zone']['role_bot_id'])
        self.channel_private_id = int(self.bot.config['Zone']['channel_private_id'])
        self.category_private_id = int(self.bot.config['Zone']['category_private_id'])

    @commands.command()
    async def create(self, ctx):
        guild = ctx.guild
        role_bot = guild.get_role(self.role_bot_id)
        category_private = guild.get_channel(self.category_private_id)

        if role_bot and category_private:
            print(0)
            if ctx.channel.id == self.channel_private_id:
                print(1)
                if f'room-{ctx.author.name}' in [ch.name for ch in guild.text_channels]:
                    print(2)
                    e_msg = discord.Embed(title=f'チャンネルは既に作成されています')
                    await ctx.reply(embed=e_msg, allowed_mentions=discord.AllowedMentions.none())
                else:
                    print(3)
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(view_channel=False),
                        ctx.author: discord.PermissionOverwrite(view_channel=True),
                        role_bot: discord.PermissionOverwrite(view_channel=True)
                    }
                    channel = await guild.create_text_channel(f'room-{ctx.author.name}',
                                                              overwrites=overwrites,
                                                              category=category_private)
                    s_msg = discord.Embed(title='プライベートチャンネルを作成しました', description=f'チャンネル: {channel.mention}')
                    await ctx.reply(embed=s_msg, allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
    bot.add_cog(Channels(bot))
