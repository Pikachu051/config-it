from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from resources import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready!')

