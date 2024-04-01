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
net_connect = None

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

async def ping(ctx, ip):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'ping {ip}')
        await ctx.send(output)

async def show_int(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show intterface')
        await ctx.send(output)

async def show_vlan_br(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show vlan brief')
        await ctx.send(output)

async def show_run(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show run')
        await ctx.send(output)
    
async def show_run_int(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show run int')
        await ctx.send(output)

async def copy_run_conf(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('copy run conf')
        await ctx.send(output)

async def hostname(ctx, hostname):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'hostname {hostname}')
        await ctx.send(output)
        
async def show_route(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show ip route')
        await ctx.send(output)
        
async def ip_route(ctx , dest_ip, dest_mark, next_hop):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'ip route {dest_ip} {dest_mark} {next_hop}')
        await ctx.send(output)
        
async def show_spanning_tree(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show spanning-tree')
        await ctx.send(output)

bot.run(TOKEN)

