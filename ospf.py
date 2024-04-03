def router_ospf(network):
        networks = networks.split(',')
        networks = [network.split('/') for network in networks]
        commands = []
        commands.append('router ospf 1')
        for network in networks:
            commands.append(f'network {network[0]} {network[1]} area {network[2]}')
        return commands