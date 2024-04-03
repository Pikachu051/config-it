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

connections = {}

def no_index_exists():
    embed = discord.Embed(title="Error", color=0xff0000)
    embed.add_field(name="", value="No device at the index provided.", inline=False)
    embed.add_field(name="", value="Use !show_connection to show all connected device with index.", inline=False)
    embed.add_field(name="", value="Use !create_connection <ip_addr> <username> <password> to connect to a device.", inline=False)
    return embed

@bot.event
async def on_ready():
    print('Bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    embed = discord.Embed(title="Bot is ready!", color=0x00ff00)
    await channel.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="Invalid command. Type **!help** to see the list of available commands.", inline=False)
        await ctx.send(embed=embed)
    else:
        raise error


@bot.command()
async def create_connection(ctx, ip, username, password):
    discord_username = str(ctx.author)

    user_connections = [key for key in connections if key.startswith(f"{discord_username}:")]
    device_index = len(user_connections) + 1

    key = f"{discord_username}:{device_index}"
    if key in connections:
        await ctx.send(f"```Device {device_index} is already connected for {discord_username}.```")
        return

    connections[key] = [ip, username, password]
    await ctx.send(f"```Connection created for {discord_username} with device #{device_index}.```")
    print(connections)

@bot.command()
async def connect(ctx, device_index: int = None):
    global net_connect
    discord_username = str(ctx.author)

    if device_index is None:
        user_connections = [key for key in connections if key.startswith(f"{discord_username}:")]
        if not user_connections:
            embed = discord.Embed(title="Error", color=0xff0000)
            embed.add_field(name="", value="You don't have any devices connected.", inline=False)
            embed.add_field(name="", value="Use !create_connection first.", inline=False)
            await ctx.send(embed=embed)
            return None
        device_index = 1

    key = f"{discord_username}:{device_index}"
    if key not in connections:
        embed = discord.Embed(title="Error", description="Device not found", color=0xff0000)
        embed.add_field(name="", value=f"No device information found for the device at index {device_index}.", inline=False)
        embed.add_field(name="", value="Use !create_connection first.", inline=False)
        await ctx.send(embed=embed)
        #await ctx.send(f"```No device information found for the device at index {device_index}.\n\nUse !create_connection first.```")
        return None

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
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="Failed to connect to device.", inline=False)
        await ctx.send(embed=embed)
        return None
    else:
        embed = discord.Embed(title="Success", color=0x00ff00)
        embed.add_field(name="", value=f"Connected to {ip} successfully!", inline=False)
        await ctx.send(embed=embed)
        return net_connect

@bot.command()
async def command_list(ctx):
    embed = discord.Embed(title="Help", description="List of available commands", color=0x00ff00)
    embed.add_field(name="!create_connection <ip> <username> <password>", value="Add a device to connection list", inline=False)
    embed.add_field(name="!show_connection", value="Show all connected devices", inline=False)
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
    await ctx.send(f'{mention}'+'``` Command lists sent to your DM!```')
    
@bot.command()
async def show_connection(ctx):
    discord_username = str(ctx.author)
    user_connections = [key for key in connections if key.startswith(f"{discord_username}:")]
    if not user_connections:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You don't have any devices connected.", inline=False)
        embed.add_field(name="", value="Use **!create_connection** first.", inline=False)
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title="Connected Devices", color=0x00ff00)
    for key in user_connections:
        device_index = key.split(":")[1]
        ip, _, _ = connections[key]
        embed.add_field(name=f"Device #{device_index}", value=f"IP: {ip}", inline=False)
    mention = ctx.author.mention
    await ctx.send(mention + '```List of connected devices has been sent to your DM!```')
    await ctx.author.send(embed=embed)

@bot.command()
async def ping(ctx, index, ip):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        await ctx.send(embed=embed)
    else:
        cmd_list = ['ping ' + ip,
                     '\n']
        await ctx.send(f'```Pinging to {ip}...```')
        output = net_connect.send_multiline_timing(cmd_list)
        count = output.count('!')
        embed = discord.Embed(title="Ping Result", color=0x00ff00)
        embed.add_field(name="Packets sent", value="5", inline=False)
        embed.add_field(name="Packets received", value=str(count), inline=False)
        embed.add_field(name="", value="----------------------", inline=False)
        embed.add_field(name="Packet received", value=f"{count} ({count * 20}% received)", inline=False)
        embed.add_field(name="Packet loss", value=f"{5 - count} ({(5 - count) * 20}% loss)", inline=False)
        await ctx.send(embed=embed)
        net_connect.disconnect()
        
@bot.command()
async def show_int(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        await ctx.send(embed=embed)
        # await ctx.send('```You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.```')
    else:
        output = net_connect.send_command('show ip int brief')
        await ctx.send('```'+output+'```')
        net_connect.disconnect()

@bot.command()
async def show_vlan(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('```You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.```')
    else:
        output = net_connect.send_command('show vlan brief')
        if 'Invalid' in output:
            await ctx.send('```This command is not supported on router.```')
        else:
            await ctx.send('```'+output+'```')
            net_connect.disconnect()

@bot.command()
async def show_run(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show run')
        await ctx.send('```'+output+'```')
        net_connect.disconnect() 

@bot.command()
async def show_run_int(ctx, index, interface):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show run int ' + interface)
        await ctx.send('```'+output+'```')
        net_connect.disconnect()

@bot.command()
async def save_config(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('wr')
        await ctx.send('```Configuration has been saved!```')
        net_connect.disconnect()

@bot.command()
async def hostname(ctx, index, hostname):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        command_list = ['hostname ' + hostname]
        output = net_connect.send_config_set(command_list)
        await ctx.send('```Hostname has been set to ' + hostname+'```')
        net_connect.disconnect()
        
@bot.command()
async def show_hostname(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
    else:
        output = net_connect.send_command('show run | include hostname')
        output = output.split(' ')[1]
        await ctx.send('```Hostname: '+output+'```')
        net_connect.disconnect()

@bot.command()
async def show_route(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f'{discord_username}:{index}'
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show ip route')
        await ctx.send('```'+output+'```')
        net_connect.disconnect()
        
@bot.command()
async def ip_route(ctx , index, dest_ip, dest_mark, next_hop):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'ip route {dest_ip} {dest_mark} {next_hop}')
        await ctx.send('```Route has been added!```')
        net_connect.disconnect()
        
@bot.command()
async def show_spanning_tree(ctx, index):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command('show spanning-tree')
        if 'No spanning tree' in output:
            embed = discord.Embed(title="Error", color=0xff0000)
            embed.add_field(name="", value=output, inline=False)
            await ctx.send(embed=embed)
        await ctx.send('```'+output+'```')
        net_connect.disconnect()

@bot.command()
async def banner(ctx, index, str):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        output = net_connect.send_command(f'banner motd # {str} #')
        await ctx.send('```Banner has been set!```')
        net_connect.disconnect()

@bot.command()
async def create_vlan(ctx, index, id):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['vlan ' + id]
        net_connect.send_config_set(configs)
        await ctx.send(f'```VLAN {id} created.```')
        net_connect.disconnect()

@bot.command()
async def vlan_ip_add(ctx, index, vlan, ip_addr, netmask):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + vlan,
                   'ip add ' + ip_addr + ' ' + netmask]
        net_connect.send_config_set(configs)
        await ctx.send(f'```IP Address {ip_addr} and Subnet Mask {netmask} has been added to VLAN {vlan}.```')
        net_connect.disconnect()

@bot.command()
async def vlan_no_shut(ctx, index, id):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['vlan ' + id,
                   'no sh']
        net_connect.send_config_set(configs)
        await ctx.send(f'```No shutdown VLAN {id} succeed.```')
        net_connect.disconnect()

@bot.command()
async def int_ip_add(ctx, index, interface, ip, mask):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'ip add ' + ip + ' ' + mask]
        net_connect.send_config_set(configs)
        await ctx.send(f'```IP Address {ip} and Subnet Mask {mask} has been added to Interface {interface}```')
        net_connect.disconnect()

@bot.command()
async def int_ip_gateway_add(ctx, index, ip_gateway):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['ip default-gateway ' + ip_gateway]
        net_connect.send_config_set(configs)
        await ctx.send(f'```IP Default Gateway {ip_gateway} has been set on the device.```')
        net_connect.disconnect()

@bot.command()
async def int_switch_mode(ctx,index, interface, mode):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        mode = mode.lower()
        configs = ['int ' + interface,
                       'switchport mode ' + mode]
        net_connect.send_config_set(configs)
        if mode == 'access':
            await ctx.send(f'```Changed {interface} to switchport mode access successfully!```')
        elif mode == 'trunk':
            await ctx.send(f'```Changed {interface} to switchport mode trunk successfully!```')
        net_connect.disconnect()

@bot.command()
async def int_no_shut(ctx,index, interface):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'no shut']
        net_connect.send_config_set(configs)
        await ctx.send(f'```Interface {interface} is now no shutdown.```')
        net_connect.disconnect()

@bot.command()
async def int_shut(ctx,index, interface):
    global net_connect
    discord_username = str(ctx.author)
    key = f"{discord_username}:{index}"
    if key not in connections:
        no_index_exists()
        return
    net_connect = await connect(ctx, index)

    if net_connect == None:
        embed = discord.Embed(title="Error", color=0xff0000)
        embed.add_field(name="", value="You need to connect to a device first!", inline=False)
        embed.add_field(name="", value="Use **!create_connect <ip> <username> <password>** to connect to a device.", inline=False)
        # await ctx.send('You need to connect to a device first!\n\nUse !connect <ip> <username> <password> to connect to a device.')
    else:
        configs = ['int ' + interface,
                   'shut']
        net_connect.send_config_set(configs)
        await ctx.send(f'```Interface {interface} is now shuted down.```')
        net_connect.disconnect()

bot.run(TOKEN)

