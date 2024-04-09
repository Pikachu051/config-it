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
        output = net_connect.send_command('show interface')
        await ctx.send(output)

async def show_vlan_br(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show vlan brief')
        await ctx.send(output)
        
async def create_vlan(ctx, id):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['vlan ' + id]
        net_connect.send_config_set(configs)
        await ctx.send(f'VLAN {id} created.')

async def vlan_ip_add(ctx, vlan, ip_addr, netmask):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + vlan,
                   'ip add ' + ip_addr + ' ' + netmask]
        net_connect.send_config_set(configs)
        await ctx.send(f'IP Address {ip_addr} and Subnet Mask {netmask} has been added to VLAN {vlan}.')
        
async def vlan_no_shut(ctx, id):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['vlan ' + id,
                   'no sh']
        net_connect.send_config_set(configs)
        await ctx.send(f'No shutdown VLAN {id} succeed.')

# ========================================================================================
# 4/1/2024

bot.run(TOKEN)

