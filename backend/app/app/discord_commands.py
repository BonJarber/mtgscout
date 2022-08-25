import discord
from discord.ext import commands

from app.core.config import settings

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def scout(ctx: commands.Context, input: str):
    await ctx.send(f"Querying {input} for data")


async def run_bot():
    try:
        await bot.start(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot.logout()
