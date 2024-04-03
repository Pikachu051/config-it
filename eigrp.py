from discord.ext import commands
import discord
from netmiko import ConnectHandler
from net_cal import wildcard_mask
# import asyncio

async def route_eigrp(networks, asn): 
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router eigrp ' + asn)
    for network in networks:
        network[1] = wildcard_mask(int(network[1]))
        commands.append (f'network {network[0]} {network[1]}')
    return commands



# async def main():
#     cmd = input()
#     asn = input()
#     result = await route_eigrp(cmd, asn)  # Call route_eigrp with both arguments and await the result
#     print(result)

# asyncio.run(main())