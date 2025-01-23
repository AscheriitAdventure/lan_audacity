from dev.project.src.classes.snmp_form import SnmpForm, PrettyData



info_device = {
    "ip_address": "192.168.90.251",
    "port": 161,
    "version": SnmpForm.SnmpVersion.SNMPv1,
    "community": "ArteEyrein"
}

snmp_form = SnmpForm(**info_device)

print(f"{snmp_form.ipAddress} {snmp_form.getIPVersion('str')}\n")

res = snmp_form.readDeviceUptime()

print(f"{res.oid}: [{res.data_type}] = {res.rawValue}")