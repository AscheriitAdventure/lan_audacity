import nmap

nm = nmap.PortScanner()
nm.scan("192.168.110.200", arguments="-sP")

print(nm["192.168.110.200"])
