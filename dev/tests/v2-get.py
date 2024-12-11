import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def fetch_snmp():
    snmp_engine = SnmpEngine()

    iterator = walk_cmd(
        snmp_engine,
        CommunityData("ArteEyrein", mpModel=1),
        await UdpTransportTarget.create(("192.168.90.250", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.2.1.4.24"))
    )

    async for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
            break
        else:
            for varBind in varBinds:
                # Si varBind[0] commence par "1.3.6.1.2.1.4.24.3"
                if str(varBind[0]).startswith("1.3.6.1.2.1.4.24.3"):
                    print(" = ".join([x.prettyPrint() for x in varBind]))
                else:
                    continue


    snmp_engine.close_dispatcher()

asyncio.run(fetch_snmp())
