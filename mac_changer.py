
import re
import subprocess
import optparse
from tabnanny import verbose
def get_arguments():
    parser=optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Specify interface to change the mac address")
    parser.add_option("-m","--mac",dest="new_mac",help="New Mac Address")
    options=parser.parse_args()[0]
    if not options.interface or not options.new_mac:
        print(parser.error("[-] Please Parse Required Options"))
    return options
def change_mac(interface,new_mac):
    print(f"[+] Changing MAC Adress for {interface} to {new_mac}")
    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",new_mac])
    subprocess.call(["ifconfig",interface,"up"])
def get_current_mac(interface):
    ifconfig_result=subprocess.check_output(["ifconfig",interface])
    mac_search_result=re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig_result))
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could Not Read Current MAC")
if __name__=="__main__":
    options=get_arguments()
    current_mac=get_current_mac(options.interface)
    print(f"[+] Current MAC = {current_mac}")
    change_mac(options.interface,options.new_mac)
    changed_mac=get_current_mac(options.interface)
    if changed_mac==options.new_mac:
        print(f"[+] MAC has been changed for {options.interface} from {current_mac} to {change_mac} ")
    else:
        print(f"[-] Could not change MAC Adress for {options.interface}")