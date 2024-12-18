#!/usr/bin/env python3
# This is  a script to scan active hosts in a network
# Import Scapy
import scapy.all as scapy

# We need to import regular expression module to make sure that input is in correct format
import re

# Basic user interface header---
print(""" 

ooooo ooooooooo.         .oooooo..o                                                                
`888' `888   `Y88.      d8P'    `Y8                                                                
 888   888   .d88'      Y88bo.       .ooooo.   .oooo.   ooo. .oo.   ooo. .oo.    .ooooo.  oooo d8b 
 888   888ooo88P'        `"Y8888o.  d88' `"Y8 `P  )88b  `888P"Y88b  `888P"Y88b  d88' `88b `888""8P 
 888   888                   `"Y88b 888        .oP"888   888   888   888   888  888ooo888  888     
 888   888              oo     .d8P 888   .o8 d8(  888   888   888   888   888  888    .o  888     
o888o o888o             8""88888P'  `Y8bod8P' `Y888""8o o888o o888o o888o o888o `Y8bod8P' d888b     
                                                                                     
""")

# Regular expression pattern to recognize ipv4 address
ip_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")

# Get the ip address range
while True:
    ip_range_entered = input("\n Enter the ip address and the range you want to scan: ")
    if ip_range_pattern.search(ip_range_entered):
        print(f"\n {ip_range_entered} is valid")
        break

# Try ARPing the ip address range supplied by the user
# The arping() method in scapy helps to create a packet with an arp message
# and then sends it to the broadcast mac address ff:ff:ff:ff:ff:ff
# If a valid ip address range was supplied the program will return the list of all results

# arp_result = scapy.arping(ip_range_entered)
# Perform the ARP scan
answered, unanswered = scapy.arping(ip_range_entered)

# Display all results
print("\nActive Hosts:")
for sent, received in answered:
    print(f"IP: {received.psrc} | MAC: {received.hwsrc}")



