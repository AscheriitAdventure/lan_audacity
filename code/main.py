from _class.cl_mdl_device import *
import nmap

def scan_lan(ip_cidr: str):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_cidr, arguments='-sn')
    active_ips = []
    for host in nm.all_hosts():
        if nm[host]['status']['state'] == 'up':
            active_ips.append(host)
    return active_ips



if __name__ == '__main__':
    device_host = MDevice(_ip='192.168.1.28', _mask='255.255.255.0')
    keywords = "Unknown"
    device_host = HostDevice()
    device_host.hostname = keywords
    print(device_host.mask)
    # device_host.mask = '0.0.0.0'
    # print(device_host.mask_to_cidr())
    # lan_host = scan_lan(device_host.mask_to_cidr())
    # print(f"{len(lan_host)} devices in LAN: {lan_host}")
