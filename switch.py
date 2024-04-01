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
async def switch(ctx, ip, subnetmask, ip_gateway, mode, access_vlan, no_shut):
    device = {
        'device_type': 'cisco_ios',
        'interface': int,
        'ip': ip,
        'ip-default gateway': ip_gateway,
        'switchport mode' : mode,
        'switchport mode acces' : access_vlan,
        'no shutdown' : no_shut,
        'port': 22,
    }
    await ctx.send(f'Connecting to {ip}...')
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show ip int brief')
    if output == '':
        await ctx.send('Failed to connect to device')
    else:
        await ctx.send(f'Connected to {ip} successfully!')


async def int_ip_add(ctx, interface, ip, mask):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'ip add ' + ip + ' ' + mask]
        net_connect.send_config_set(configs)
        await ctx.send('IP Address ' + ip + ' and Subnet Mask ' + mask + ' has been added to Interface ' + interface)

async def int_ip_gateway_add(ctx, ip_gateway):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['ip-default gateway ' + ip_gateway]
        net_connect.send_config_set(configs)
        await ctx.send('IP-default gateway ' + ip_gateway + ' has been added to switch')

async def int_switch_mode(ctx, mode):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        mode = mode.lower()
        if mode == 'access':
            configs = ['switchport mode ' + mode]
            net_connect.send_config_set(configs)
            await ctx.send('Change to switchport mode access successfully!')
        elif mode == 'trunk':
            configs = ['switchport mode ' + mode]
            net_connect.send_config_set(configs)
            await ctx.send('Change to switchport mode trunk successfully!')

async def int_no_shut(ctx, interface):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'no shut']
        net_connect.send_config_set(configs)
        await ctx.send('Interface ' + interface + ' is no shutdown')

# ========================================================================================
# 4/1/2024


bot.run(TOKEN)

