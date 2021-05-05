import discord
import math
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bot'])
    async def bot_count(self, ctx):
        count = len([x.name for x in ctx.guild.members if x.bot])
        await ctx.reply(f'導入BOT数: {count}', allowed_mentions=discord.AllowedMentions.none())

    @commands.command(aliases=['user', 'member'])
    async def user_count(self, ctx):
        count = len([x.name for x in ctx.guild.members if not x.bot])
        await ctx.reply(f'メンバー数: {count}', allowed_mentions=discord.AllowedMentions.none())

    @commands.command(aliases=['ch'])
    async def channel_count(self, ctx):
        count = len(ctx.guild.channels)
        await ctx.reply(f'チャンネル数: {count}', allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            description=f' Pong! - {math.floor(self.bot.latency * 1000)} ms'
        )
        await ctx.reply(embed=embed, allowed_mentions=discord.AllowedMentions.none())
