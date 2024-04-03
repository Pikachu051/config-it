import math

def subnet_mask(subnet_mask):
    
    # Calculate the subnet mask in IPv4 format
    mask = 0xffffffff ^ (0xffffffff >> subnet_mask)
    subnet_mask_ipv4 = '{}.{}.{}.{}'.format(
        (mask >> 24) & 0xff,
        (mask >> 16) & 0xff,
        (mask >> 8) & 0xff,
        mask & 0xff
    )
    
    return subnet_mask_ipv4


def wildcard_mask(subnet_mask):

    host_bits = 32 - subnet_mask
    
    # Calculate the wildcard mask in IPv4 format
    wildcard_mask = (0xffffffff >> (32 - host_bits)) & 0xffffffff
    wildcard_mask_ipv4 = '{}.{}.{}.{}'.format(
        (wildcard_mask >> 24) & 0xff,
        (wildcard_mask >> 16) & 0xff,
        (wildcard_mask >> 8) & 0xff,
        wildcard_mask & 0xff
    )
    
    return wildcard_mask_ipv4