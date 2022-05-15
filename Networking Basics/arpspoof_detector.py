import scapy.all as scapy
def get_mac(IP):
    arp_request = scapy.ARP(pdst=IP)
    broadcost = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcost = broadcost / arp_request
    answered_list = scapy.srp(arp_request_broadcost, timeout=1, verbose=False)[0]
    if len(answered_list)>=1:
        return answered_list[0][1].hwsrc
def sniff():
    scapy.sniff(store=False,prn=process_sniffed_packet) # sniff packet using scapy
def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2:
        try:
            real_mac=get_mac(packet[scapy.ARP].psrc)
            if real_mac:
                received_response_mac=packet[scapy.ARP].hwsrc
                if real_mac!=received_response_mac:
                    print("[-] You are under attack !!")
        except IndexError :
            pass
if __name__=="__main__":
    print()