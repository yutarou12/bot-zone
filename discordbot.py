import discord
import traceback
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(
    command_prefix='test!',
    intents=intents
)

config = {
    'Zone': {
        'guild_id': os.getenv("GUILD_ID"),
        'log_channel_id': os.getenv("LOG_CHANNEL_ID"),
        'welcome_channel_id': os.getenv("WELCOME_CHANNEL_ID"),
        'role_member_id': os.getenv("ROLE_MEMBER_ID"),
        'role_bot_id': os.getenv("ROLE_BOT_ID"),
        'channel_private_id': os.getenv("CHANNEL_PRIVATE_ID"),
        'category_private_id': os.getenv("CATEGORY_PRIVATE_ID"),
    }
}


@bot.event
async def on_ready():
    print(f"{bot.user.name} でログインしました")
    await bot.change_presence(activity=discord.Game(name=f"BotZone OfficialBOT | {bot.command_prefix}", type=1))
    ch = bot.get_channel(int(config['Zone']['log_channel_id']))
    bot_count = len([x.name for x in ch.guild.members if x.bot])
    member_count = len([x.name for x in ch.guild.members if not x.bot])

    log_msg = discord.Embed(title="BB起動Log", description="Bot が起動しました")
    log_msg.add_field(name=f"{ch.guild.name} に参加している人数",
                      value=f"{member_count}",
                      inline=False)
    log_msg.add_field(name=f"{ch.guild.name} のBOTの導入数",
                      value=f"{bot_count}",
                      inline=False)
    log_msg.set_thumbnail(url=bot.user.avatar_url)
    await ch.send(embed=log_msg)


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(f"```\n{error_msg}\n```")
    app_info = await bot.application_info()
    await app_info.owner.send(f"エラー情報\n```\n{error_msg}\n```")

if __name__ == '__main__':
    bot.config = config
    extensions = [
        'cogs.admin',
        'cogs.utils',
        'cogs.join',
        'cogs.leave',
        'cogs.channels'
    ]
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
