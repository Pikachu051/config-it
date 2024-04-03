from discord.ext import commands
import discord
from netmiko import ConnectHandler

async def route_eigrp(ctx, index, asn, networks): 
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router eigrp' + asn)
    for network in networks:
        commands.append (f'network {network[0]} {network[1]}')
    return commands