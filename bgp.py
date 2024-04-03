from discord.ext import commands
import discord
from netmiko import ConnectHandler


def bgp(networks, neighbors, asn):
    
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router bgp ' + asn)
    for network in networks:
        commands.append(f'network {network[0]} mask {network[1]}')
    neighbors = neighbors.split(',')
    neighbors = [neighbor.split(':') for neighbor in neighbors]
    for neighbor in neighbors:
        commands.append(f'neighbor {neighbor[0]} remote-as {neighbor[1]}')
    return commands
