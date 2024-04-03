from discord.ext import commands
import discord
from netmiko import ConnectHandler
from net_cal import wildcard_mask

def ospf(networks):
        networks = networks.split(',')
        networks = [network.split('/') for network in networks]
        commands = []
        commands.append('router ospf 1')
        for network in networks:
            network[1] = wildcard_mask(int(network[1]))
            commands.append(f'network {network[0]} {network[1]} area {network[2]}')
        return commands
