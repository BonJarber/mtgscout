import discord
import validators
from urllib.parse import urlparse
from discord.ext import commands

from app.core.config import settings
from app.stores.card_kingdom import parse_cardkingdom_url

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def scout(ctx: commands.Context, input_sr: str):
    if validators.url(input_sr):
        url = urlparse(input_sr)
        if not url:
            await ctx.send(
                f"Could not properly parse the URL, double check and try again"
            )
        if url.netloc == "www.cardkingdom.com":
            result = parse_cardkingdom_url(url)
            await ctx.send(result)


async def run_bot():
    try:
        await bot.start(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot.logout()
