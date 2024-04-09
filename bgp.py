from discord.ext import commands
import discord
from netmiko import ConnectHandler
from net_cal import subnet_mask

def bgp(networks, neighbors, asn):
    
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router bgp ' + asn)
    
    for network in networks:
        network[1] = subnet_mask(int(network[1]))
        commands.append(f'network {network[0]} mask {network[1]}')
    neighbors = neighbors.split(',')
    neighbors = [neighbor.split(':') for neighbor in neighbors]
    for neighbor in neighbors:
        commands.append(f'neighbor {neighbor[0]} remote-as {neighbor[1]}')
    return commands

def remove_bgp_nw(networks, asn):
    networks = networks.split(',')
    networks = [network.split('/') for network in networks]
    commands = []
    commands.append('router bgp ' + asn)
    for network in networks:
        network[1] = subnet_mask(int(network[1]))
        commands.append(f'no network {network[0]} mask {network[1]}')
    return commands

def remove_bgp_neighbor(neighbors, asn):
    neighbors = neighbors.split(',')
    commands = []
    commands.append('router bgp ' + asn)
    neighbors = [neighbor.split(':') for neighbor in neighbors]
    for neighbor in neighbors:
        commands.append(f'no neighbor {neighbor[0]} remote-as {neighbor[1]}')
    return commands

def disable_bgp(asn):
    return ['no router bgp ' + asn]
