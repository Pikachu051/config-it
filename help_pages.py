import discord

embed1 = discord.Embed(title="Help (1/5)", description="List of available commands:", color=0x00ff00)
embed1.add_field(name="!create_connection <ip> <username> <password>", value="Add a device to connection list", inline=False)
embed1.add_field(name="!show_connection", value="Show all connected devices", inline=False)
embed1.add_field(name="!ping <ip_dest>", value="Ping an IP address", inline=False)
embed1.add_field(name="!show_hostname", value="Show hostname of a device", inline=False)
embed1.add_field(name="!show_int", value="Show interface status", inline=False)
embed1.add_field(name="!show_vlan", value="Show VLAN information", inline=False)
embed1.add_field(name="!show_run", value="Show running configuration", inline=False)
embed1.add_field(name="!show_run_int <interface>", value="Show interface configuration", inline=False)
embed1.add_field(name="!save_config", value="Save running configuration", inline=False)
embed1.add_field(name="!hostname <hostname>", value="Set device hostname", inline=False)

embed2 = discord.Embed(title="Help (2/5)", description="List of available commands:", color=0x00ff00)
embed2.add_field(name="!show_route", value="Show IP routing table", inline=False)
embed2.add_field(name="!ip_route <dest_ip> <dest_mark> <next_hop>", value="Add IP route", inline=False)
embed2.add_field(name="!show_spanning_tree", value="Show spanning tree information", inline=False)
embed2.add_field(name="!banner <str>", value="Set banner message", inline=False)
embed2.add_field(name="!create_vlan <vlan_number>", value="Create a new VLAN", inline=False)
embed2.add_field(name="!vlan_ip_add <vlan_number> <ip_addr> <netmask>", value="Add IP address to VLAN", inline=False)
embed2.add_field(name="!vlan_no_shut <vlan_number>", value="No shutdown VLAN", inline=False)
embed2.add_field(name="!delete_vlan <vlan_number>", value="Delete VLAN", inline=False)
embed2.add_field(name="!int_ip_add <interface> <ip> <mask>", value="Add IP address to interface", inline=False)
embed2.add_field(name="!int_ip_gateway_add <ip_gateway>", value="Set default gateway", inline=False)

embed3 = discord.Embed(title="Help (3/5)", description="List of available commands:", color=0x00ff00)
embed3.add_field(name="!delete_gateway <ip_gateway>", value="Delete default gateway", inline=False)
embed3.add_field(name="!int_switch_mode <interface> <mode>", value="Set interface switchport mode", inline=False)
embed3.add_field(name="!int_no_shut <interface>", value="No shutdown interface", inline=False)
embed3.add_field(name="!int_shut <interface>", value="Shutdown interface", inline=False)
embed3.add_field(name="", value="", inline=False)
embed3.add_field(name="!rip <network>", value="Create/Add RIP network", inline=False)
embed3.add_field(name="!remove_rip_nw <network>", value="Remove RIP network", inline=False)
embed3.add_field(name="!disable_rip", value="Disable RIP Routing Protocol", inline=False)
embed3.add_field(name="!show_rip", value="show ip rip neighbor", inline=False)
embed3.add_field(name="", value="", inline=False)
embed3.add_field(name="!ospf <network>", value="Create/Add OSPF network", inline=False)
embed3.add_field(name="!remove_ospf_nw <network>", value="Remove OSPF network", inline=False)
embed3.add_field(name="!disable_ospf", value="Disable OSPF Routing Protocol", inline=False)
embed3.add_field(name="!show_ospf", value="show ip ospf neighbor", inline=False)

embed4 = discord.Embed(title="Help (4/5)", description="List of available commands:", color=0x00ff00)
embed4.add_field(name="!eigrp <network>", value="Create/Add EIGRP network", inline=False)
embed4.add_field(name="!remove_eigrp_nw <network>", value="Remove EIGRP network", inline=False)
embed4.add_field(name="!disable_eigrp", value="Disable EIGRP Routing Protocol", inline=False)
embed4.add_field(name="!show_eigrp", value="show ip eigrp neighbor", inline=False)
embed4.add_field(name="", value="", inline=False)
embed4.add_field(name="!bgp <network>", value="Create/Add BGP network", inline=False)
embed4.add_field(name="!remove_bgp_nw <network>", value="Remove BGP network", inline=False)
embed4.add_field(name="!remove_bgp_neighbor <neighbor>", value="Remove BGP neighbor", inline=False)
embed4.add_field(name="!disable_bgp", value="Disable BGP Routing Protocol", inline=False)
embed4.add_field(name="!show_bgp", value="show ip bgp summary", inline=False)
embed4.add_field(name="", value="", inline=False)
embed4.add_field(name="!delete_route", value="Delete route", inline=False)
embed4.add_field(name="!vlan_ip_delete", value="Delete IP from the specified VLAN", inline=False)
embed4.add_field(name="!int_ip_delete", value="Delete IP from the specified interface", inline=False)

embed5 = discord.Embed(title="Help (5/5)", description="List of available commands:", color=0x00ff00)
embed5.add_field(name="!Show_cbp_neighbor", value="Show CDP neighbor", inline=False)
embed5.add_field(name="!Show_mac_table", value="Show MAC Address table", inline=False)
embed5.add_field(name="!vlan_shut", value="Shutdown VLAN", inline=False)
embed5.add_field(name="!router_on_a_stick", value="Create sub-interface on a router", inline=False)




pages = [embed1, embed2, embed3, embed4, embed5]

def get_help_page(num):
    return pages[num-1]