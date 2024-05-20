from _src._class.model_list import DeviceManager, NetDevice
import nmap


def scan_network():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')
    return nm.all_hosts()

if __name__ == '__main__':
    all_device = DeviceManager()
    all_hosts = scan_network()
    print("Nombre total d'hôtes sur le réseau:", len(all_hosts))
    for host in all_hosts:
        device = NetDevice(ip=host, mask='255.255.255.0')
        device.set_name()
        device.set_mask()
        device.set_addrMac()
        print(f"{device.__str__()}\n{device.clocktime.__str__()}")
        all_device.add_device(device)
