import scapy.all as scapy

"""
scan(IP): scan active IPs  within LAN network
-> send ARP request to every IP in network
-> active IPs will send response of request
-> return list of active IPs
"""

def scan(IP):
    arp_request=scapy.ARP(pdst=IP)
    broadcost=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcost=broadcost/arp_request
    answered_list=scapy.srp(arp_request_broadcost,timeout=1,verbose=False)[0]
    client_list=[]
    for element in answered_list:
        client_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

"""
print(): print result of scanned IPs returned from scan function
"""
def print_result(result_list):
    print("IP\t\t\t\tMAC")
    print("-"*40)
    for client in result_list:
        print(client["ip"]+"\t\t"+client["mac"])
    print("-"*40)
    print(f"[+] Found {len(result_list)} Active Devices.")
if __name__=="__main__":
    scan_result=scan("10.5.21.1/22")
    print_result(scan_result)