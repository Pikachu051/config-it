from discord.ext import commands
import discord
from netmiko import ConnectHandler
from net_cal import wildcard_mask
# import asyncio

async def eigrp(networks, asn): 
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router eigrp ' + asn)
    for network in networks:
        network[1] = wildcard_mask(int(network[1]))
        commands.append (f'network {network[0]} {network[1]}')
    return commands

def remove_eigrp_nw(networks, asn):
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router eigrp ' + asn)
    for network in networks:
        network[1] = wildcard_mask(int(network[1]))
        commands.append(f'no network {network[0]} {network[1]}')
    return commands

def disable_eigrp(asn):
    return ['no router eigrp '+ asn]



# async def main():
#     cmd = input()
#     asn = input()
#     result = await route_eigrp(cmd, asn)  # Call route_eigrp with both arguments and await the result
#     print(result)

# asyncio.run(main())