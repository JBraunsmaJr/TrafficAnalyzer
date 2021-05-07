#!/usr/bin/env python
import pyfiglet as pyfiglet
import scapy.all as scapy
import prettytable

ascii_banner = pyfiglet.figlet_format("NETWORK SCANNER")
print(ascii_banner)


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list


def print_result(results_list):
    prettytable.field_names = ["IP", "MAC"]
    for client in results_list:
        print(client)


# x = input("Enter valid IPv4 address or subnet. (Example: 192.168.0.1/24 or 192.168.0.10): ")

scan_result = scan("192.168.0.1/24")
print_result(scan_result)
