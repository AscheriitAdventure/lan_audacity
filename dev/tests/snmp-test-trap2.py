from dev.project.src.classes.snmp_form import SnmpForm, PrettyData



info_device = {
    "ip_address": "192.168.1.250",
    "port": 161,
    "version": SnmpForm.SnmpVersion.SNMPv2c,
    "community": "ArteEyrein"
}

snmp_form = SnmpForm(**info_device)

print(f"{snmp_form.ipAddress} {snmp_form.getIPVersion('str')}\n")

result: list = snmp_form.readDeviceUptime()

for data in result:
    print(data.data_type)
    print(data.getOIDText())