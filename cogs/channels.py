import discord
import asyncio
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
            if ctx.channel.id == self.channel_private_id:
                if f'room-{ctx.author.name}' in [ch.name for ch in guild.text_channels]:
                    e_msg = discord.Embed(title=f'チャンネルは既に作成されています')
                    await ctx.reply(embed=e_msg, allowed_mentions=discord.AllowedMentions.none())
                else:
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

    @commands.command()
    async def clean(self, ctx):
        guild = ctx.guild
        category_private = guild.get_channel(self.category_private_id)

        if category_private:
            if ctx.channel.id == self.channel_private_id:
                user_channel = [ch for ch in guild.text_channels if ch.name == f'room-{ctx.author.name}']
                if user_channel:
                    e_msg = discord.Embed(title=f'チャンネの再生成',
                                          description="再生成する場合は`y`、キャンセルする場合は`n`を送信してください")
                    re_msg = await ctx.reply(embed=e_msg, allowed_mentions=discord.AllowedMentions.none())

                    def check(message):
                        if message.author == ctx.author and (message.content in ["y", "n"]):
                            return message.content
                    try:
                        msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                    except asyncio.TimeoutError:
                        await re_msg.edit(discord.Embed(description='時間切れです'))

                    if msg.content == 'y':
                        await msg.delete()
                        new_channel = await user_channel[0].clone(name=f'room-{ctx.author.name}')
                        await user_channel[0].delete()
                        await re_msg.edit(embed=discord.Embed(title='再生成しました',
                                                              description=f'チャンネル: {new_channel.mention}'))
                    elif msg.content == 'n':
                        await msg.delete()
                        await re_msg.edit(embed=discord.Embed(description='キャンセルしました'))
                    else:
                        pass
                else:
                    await ctx.reply(embed=discord.Embed(description="プライベートチャンネルが見つかりません"),
                                    allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
    bot.add_cog(Channels(bot))
