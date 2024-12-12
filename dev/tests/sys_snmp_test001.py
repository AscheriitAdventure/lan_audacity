from dev.project.src.classes.snmp_form import SnmpForm, PrettyData
import asyncio


form_snmp = {
    "ip_address": "192.168.90.251",
    "port": 161,
    "version": SnmpForm.SnmpVersion.SNMPv2c,
    "community": "ArteEyrein"
}

# oid = "1.3.6.1.2.1.4.24.3"
oid = "1.3.6.1.2.1.1"

cmd_snmp = SnmpForm(**form_snmp)


async def main():
    result_data = await cmd_snmp.getWalkOID(oid)
    print(result_data)
    for res in result_data:
        print(f"{res.oid}: [{res.data_type}] = {res.rawValue}")

asyncio.run(main())

print(cmd_snmp.getIPVersion('int'))
