def router_rip(network):
    configs = ['router rip', 'version 2', 'no auto-summary']
    networks = network.split(',')
    for network in networks:
        configs.append('network ' + network)
    return configs
