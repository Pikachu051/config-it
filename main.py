from typing import Final
import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from netmiko import ConnectHandler
import time

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
    global net_connect
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

@bot.command()
async def ping(ctx, ip):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'ping {ip}', read_timeout=20)
        time.sleep(10)
        count = 0
        for line in output.split('\n'):
            if '!' in line:
                count += 1
        await ctx.send('Packets sent: 5, Packets received: ' + str(count) + ', Packet loss: ' + str(5 - count) + ' (' + str((5 - count) * 20) + '% loss)')

@bot.command()
async def show_int(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show ip int brief')
        await ctx.send(output)

@bot.command()
async def show_vlan(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show vlan brief')
        if 'Invalid' in output:
            await ctx.send('This command is not supported on router.')
        else:
            await ctx.send(output)

@bot.command()
async def show_run(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show run')
        await ctx.send(output)   

@bot.command()
async def show_run_int(ctx, interface):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show run int ' + interface)
        await ctx.send('Configuration has been saved!')

@bot.command()
async def save_config(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('wr')
        await ctx.send(output)

@bot.command()
async def hostname(ctx, hostname):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'hostname {hostname}')
        await ctx.send('Hostname has been set to ' + hostname)
        
@bot.command()
async def show_route(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show ip route')
        await ctx.send(output)
        
@bot.command()
async def ip_route(ctx , dest_ip, dest_mark, next_hop):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'ip route {dest_ip} {dest_mark} {next_hop}')
        await ctx.send('Route has been added!')
        
@bot.command()
async def show_spanning_tree(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show spanning-tree')
        await ctx.send(output)

@bot.command()
async def banner(ctx, str):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'banner motd # {str} #')
        await ctx.send('Banner has been set!')

@bot.command()
async def create_vlan(ctx, id):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['vlan ' + id]
        net_connect.send_config_set(configs)
        await ctx.send(f'VLAN {id} created.')

@bot.command()
async def vlan_ip_add(ctx, vlan, ip_addr, netmask):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + vlan,
                   'ip add ' + ip_addr + ' ' + netmask]
        net_connect.send_config_set(configs)
        await ctx.send(f'IP Address {ip_addr} and Subnet Mask {netmask} has been added to VLAN {vlan}.')

@bot.command()
async def vlan_no_shut(ctx, id):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['vlan ' + id,
                   'no sh']
        net_connect.send_config_set(configs)
        await ctx.send(f'No shutdown VLAN {id} succeed.')

@bot.command()
async def int_ip_add(ctx, interface, ip, mask):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'ip add ' + ip + ' ' + mask]
        net_connect.send_config_set(configs)
        await ctx.send('IP Address ' + ip + ' and Subnet Mask ' + mask + ' has been added to Interface ' + interface)

@bot.command()
async def int_ip_gateway_add(ctx, ip_gateway):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['ip-default gateway ' + ip_gateway]
        net_connect.send_config_set(configs)
        await ctx.send('IP-default gateway ' + ip_gateway + ' has been added to switch')

@bot.command()
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

@bot.command()
async def int_no_shut(ctx, interface):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'no shut']
        net_connect.send_config_set(configs)
        await ctx.send('Interface ' + interface + ' is no shutdown')


bot.run(TOKEN)

