from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from netmiko import ConnectHandler

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
CHANNEL_ID: Final[int] = int(os.getenv("CHANNEL_ID"))

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Bot is ready!')

@bot.command()
async def connect(ctx, ip, username, password):
    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
        'port': 22,
    }
    await ctx.send(f'Connecting to {ip}...')
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show ip int brief')
    if output == '':
        await ctx.send('Failed to connect to device')
    else:
        await ctx.send(f'Connected to {ip} successfully!')


bot.run(TOKEN)

