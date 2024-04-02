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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command. Type !help to see the list of available commands.')
    else:
        raise error

connections = {}

async def create_connection(ctx, ip, username, password):
    discord_username = str(ctx.author)
    tagline = ctx.author.discriminator

    user_connections = [key for key in connections if key.startswith(f"{discord_username}#{tagline}:")]
    device_index = len(user_connections) + 1

    key = f"{discord_username}#{tagline}:{device_index}"
    if key in connections:
        await ctx.send(f"```Device {device_index} is already connected for {discord_username}#{tagline}.```")
        return

    connections[key] = [ip, username, password]
    await ctx.send(f"```Connection created for {discord_username}#{tagline} with device {device_index}.```")

@bot.command()
async def connect(ctx, device_index: int = None):
    discord_username = str(ctx.author)
    tagline = ctx.author.discriminator

    if device_index is None:
        user_connections = [key for key in connections if key.startswith(f"{discord_username}#{tagline}:")]
        if not user_connections:
            await ctx.send("```You don't have any devices connected.\n\nUse !create_connection first.```")
            return
        device_index = 1

    key = f"{discord_username}#{tagline}:{device_index}"
    if key not in connections:
        await ctx.send(f"```No device information found for the device at index {device_index}.\n\nUse !create_connection first.```")
        return

    ip, username, password = connections[key]

    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
        'port': 22,
    }

    await ctx.send(f'```Connecting to {ip}...```')
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show ip int brief')
    if output == '':
        await ctx.send('```Failed to connect to device```')
    else:
        await ctx.send(f'```Connected to {ip} successfully!```')
        connections[key].append(net_connect)

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
    await ctx.send(f'```Connecting to {ip}...```')
    try:
        net_connect = ConnectHandler(**device)
        await ctx.send(f'```Connected to {ip} successfully!```')
    except Exception as e:
        print('```Failed to connect to the device.```')

@bot.command()
async def command_list(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    embed.add_field(name="!connect <ip> <username> <password>", value="Connect to a network device", inline=False)
    embed.add_field(name="!ping <ip>", value="Ping an IP address", inline=False)
    embed.add_field(name="!show_int", value="Show interface status", inline=False)
    embed.add_field(name="!show_vlan", value="Show VLAN information", inline=False)
    embed.add_field(name="!show_run", value="Show running configuration", inline=False)
    embed.add_field(name="!show_run_int <interface>", value="Show interface configuration", inline=False)
    embed.add_field(name="!save_config", value="Save running configuration", inline=False)
    embed.add_field(name="!hostname <hostname>", value="Set device hostname", inline=False)
    embed.add_field(name="!show_route", value="Show IP routing table", inline=False)
    embed.add_field(name="!ip_route <dest_ip> <dest_mark> <next_hop>", value="Add IP route", inline=False)
    embed.add_field(name="!show_spanning_tree", value="Show spanning tree information", inline=False)
    embed.add_field(name="!banner <str>", value="Set banner message", inline=False)
    embed.add_field(name="!create_vlan <id>", value="Create a new VLAN", inline=False)
    embed.add_field(name="!vlan_ip_add <vlan> <ip_addr> <netmask>", value="Add IP address to VLAN", inline=False)
    embed.add_field(name="!vlan_no_shut <id>", value="No shutdown VLAN", inline=False)
    embed.add_field(name="!int_ip_add <interface> <ip> <mask>", value="Add IP address to interface", inline=False)
    embed.add_field(name="!int_ip_gateway_add <ip_gateway>", value="Set default gateway", inline=False)
    embed.add_field(name="!int_switch_mode <interface> <mode>", value="Set interface switchport mode", inline=False)
    embed.add_field(name="!int_no_shut <interface>", value="No shutdown interface", inline=False)
    embed.add_field(name="!int_shut <interface>", value="Shutdown interface", inline=False)
    
    mention = ctx.author.mention
    await ctx.author.send(embed=embed)
    await ctx.send(f'```{mention}, Command lists sent to your DM!```')

@bot.command()
async def ping(ctx, ip):
    if net_connect == None:
        await ctx.send('```You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.```')
    else:
        output = net_connect.send_command_timing(f'ping {ip}', last_read=10.0)
        await ctx.send(f'```Pinging to {ip}...```')
        count = 0
        for line in output.split('\n'):
            if '!' in line:
                count += 1
        await ctx.send('```Packets sent: 5, Packets received: ' + str(count) + ', Packet loss: ' + str(5 - count) + ' (' + str((5 - count) * 20) + '% loss)```')

@bot.command()
async def show_int(ctx):
    if net_connect == None:
        await ctx.send('```You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.```')
    else:
        output = net_connect.send_command('show ip int brief')
        await ctx.send(output)

@bot.command()
async def show_vlan(ctx):
    if net_connect == None:
        await ctx.send('```You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.```')
    else:
        output = net_connect.send_command('show vlan brief')
        if 'Invalid' in output:
            await ctx.send('```This command is not supported on router.```')
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
        await ctx.send(output)

@bot.command()
async def save_config(ctx):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('wr')
        await ctx.send('Configuration has been saved!')

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
        configs = ['ip default-gateway ' + ip_gateway]
        net_connect.send_config_set(configs)
        await ctx.send('IP Default Gateway ' + ip_gateway + ' has been set on the device.')

@bot.command()
async def int_switch_mode(ctx, interface, mode):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        mode = mode.lower()
        configs = ['int ' + interface,
                       'switchport mode ' + mode]
        net_connect.send_config_set(configs)
        if mode == 'access':
            await ctx.send('Changed ' + interface + ' to switchport mode access successfully!')
        elif mode == 'trunk':
            await ctx.send('Changed ' + interface + ' to switchport mode trunk successfully!')

@bot.command()
async def int_no_shut(ctx, interface):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'no shut']
        net_connect.send_config_set(configs)
        await ctx.send('Interface ' + interface + ' is now no shutdown.')

@bot.command()
async def int_shut(ctx, interface):
    if net_connect == None:
        await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'shut']
        net_connect.send_config_set(configs)
        await ctx.send('Interface ' + interface + ' is now shuted down.')

bot.run(TOKEN)

