import json

from dev.project.core.db_def_prod import createDeviceType


def generateDeviceTypeDefault(sqlServer, file):
    with open(file, "r", encoding="utf-8") as file:
        deviceTypes = json.load(file)
    
    for deviceType in deviceTypes:
        name = deviceType.get("name")
        osiProtocol = deviceType.get("osi_layer")
        pixmapPath = deviceType.get("pixmap_path")
        description = deviceType.get("description")

        createDeviceType(sqlServer, name, osiProtocol, pixmapPath, description)

    
