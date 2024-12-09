# Conventions MIB

## Internet Assigned Numbers Authority (IANA)

### IANAifType

Found in OID: 1.3.6.1.2.1.2.2.1.3  
OID Text: iso. org. dod. internet. mgmt. mib-2. interfaces. ifTable. ifEntry. ifType.

Syntax: IANAifType (IANAifType-MIB)

[URL Link](https://simpleweb.org/ietf/mibs/modules/html/right.php?category=IANA&module=IANAifType-MIB&object=IANAifType&isNoOid=1)

#### Description

This data type is used as the syntax of the ifType object in the (updated) definition of MIB-II's ifTable.

The definition of this textual convention with the addition of newly assigned values is published periodically by the IANA, in either the Assigned Numbers RFC, or some derivative of it specific to Internet Network Management number assignments. (The latest arrangements can be obtained by contacting the IANA.)

Requests for new values should be made to IANA via email (iana@iana.org).

The relationship between the assignment of ifType values and of OIDs to particular media-specific MIBs is solely the purview of IANA and is subject to change without notice.
Quite often, a media-specific MIB's OID-subtree assignment within MIB-II's 'transmission' subtree will be the same as its ifType value.  
However, in some circumstances this will not be the case, and implementors must not pre-assume any specific relationship between ifType values and transmission subtree OIDs.

#### Syntax

Returns an **`INTEGER`** value but this is a false _`Enum Table`_

## IF-MIB

### Tag `ifOperStatus`

Found in OID: 1.3.6.1.2.1.2.2.1.8  
OID Text: iso. org. dod. internet. mgmt. mib-2. interfaces. ifTable. ifEntry. ifOperStatus.

Syntax: Enum

#### Description

The current operational state of the interface.
The testing(3) state indicates that no operational packets can be passed.
If ifAdminStatus is down(2) then ifOperStatus should be down(2).
If ifAdminStatus is changed to up(1) then ifOperStatus should change to up(1) if the interface is ready to transmit and receive network traffic; it should change to dormant(5) if the interface is waiting for external actions (such as a serial line waiting for an incoming connection); it should remain in the down(2) state if and only if there is a fault that prevents it from going to the up(1) state; it should remain in the notPresent(6) state if the interface has missing (typically, hardware) components.

#### Enum Table

```python
from enum import Enum

class ifOperStatusMIB(Enum):
    up = 1
    down = 2
    testing = 3
    unknown = 4
    dormant = 5
    notPresent = 6
    lowerLayerDown = 7
```

### Tag `ifSpeed`

Found in OID: 1.3.6.1.2.1.2.2.1.5  
OID Text: iso. org. dod. internet. mgmt. mib-2. interfaces. ifTable. ifEntry. ifSpeed.

Syntax: Gauge32 (SNMPv2-SMI)

[URL Link](https://simpleweb.org/ietf/mibs/modules/html/rDef.php?category=IETF&module=SNMPv2-SMI&object=Gauge32&do=1)

#### Description

An estimate of the interface's current bandwidth in bits per second.
For interfaces which do not vary in bandwidth or for those where no accurate estimation can be made, this object should contain the nominal bandwidth.
If the bandwidth of the interface is greater than the maximum value reportable by this object then this object should report its maximum value (4,294,967,295) and ifHighSpeed must be used to report the interface's speed.
For a sub-layer which has no concept of bandwidth, this object should be zero.

#### Syntax

Returns an **`UNSIGNED INT 32 BIT`** (0 to 4294967295)

### Tag `sysServices`

Found at OID: 1.3.6.1.2.1.1.7  
OID Text: iso. org. dod. internet. mgmt. mib-2. system. sysServices.

Syntax: Integer32 (0...127)

#### Description

A value which indicates the set of services that this entity may potentially offer.
The value is a sum.  
This sum initially takes the value zero.
Then, for each layer, $L$, in the range 1 through 7, that this node performs transactions for, $2^{(L - 1)}$ is added to the sum.
For example, a node which performs only routing functions would have a value of $4 = 2^{(3-1)}$.
In contrast, a node which is a host offering application services would have a value of $72 = 2^{(4-1)} + 2^{(7-1)}$.  
Note that in the context of the Internet suite of protocols, values should be calculated accordingly :
| layer | functionality                          |
| :---: | :------------------------------------- |
|   1   | physical (e.g., repeaters)             |
|   2   | datalink/subnetwork (e.g., bridges)    |
|   3   | internet (e.g., supports the IP)       |
|   4   | end-to-end (e.g., supports the TCP)    |
|   7   | applications (e.g., supports the SMTP) |

For systems including OSI protocols, layers 5 and 6 may also be counted.

#### Code Translate

```python
from enum import Enum
from typing import List


class OSILayer(Enum):
    PHYSICAL = 1        # physical (e.g., repeaters)
    DATA_LINK = 2       # datalink/subnetwork (e.g., bridges)
    NETWORK = 3         # internet (e.g., supports the IP)
    TRANSPORT = 4       # end-to-end (e.g., supports the TCP)
    SESSION = 5         # 
    PRESENTATION = 6    #
    APPLICATIONS = 7    # applications (e.g., supports the SMTP)


def sysServicesList(tag_oid: int) -> List[str]:
    """
    Returns a list of services (OSI layers) based on the numeric value (tag_oid).
    """
    services = []
    if tag_oid == 0:
        services.append("Do not possess this information")
    else:
        for layer in OSILayer:
            # Check if the bit corresponding to the layer is set
            if tag_oid & (1 << (layer.value - 1)):
                services.append(layer.name)

    return services


# Example usage
if __name__ == "__main__":
    test_value = 6  # Example value to analyze
    result = sysServicesList(test_value)
    print(f"Services for tag_oid {test_value}: {result}")
```

### 