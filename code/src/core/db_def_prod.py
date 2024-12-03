from typing import Optional
from src.core.sql_server import MySQLConnection as SQLServer
import time
import logging
import uuid
from typing import Optional, List, Any

# --- Insertion de données dans la base de données ---


def createClock(srv_db: SQLServer) -> int:
    sql = "INSERT INTO clockmanager (created_at, updated_at, type_time) VALUES "
    values = f"({time.time()}, {time.time()}, 'Unix Timestamp Format');"
    query = sql + values
    return srv_db.execute_query_id(query)


def updateClock(srv_db: SQLServer, clock_id: int):
    timeclock = time.time()
    # Insert new update
    sql_1 = "INSERT INTO updateatlist (clock_manager_id, updated_at) VALUES "
    values = f"({clock_id}, {timeclock});"
    query_1 = sql_1 + values
    srv_db.execute_query(query_1)

    # Update clock
    sql_2 = f"UPDATE clockmanager SET updated_at = {
        timeclock} WHERE id = {clock_id};"
    srv_db.execute_query(sql_2)


def createUser(srv_db: SQLServer, name: str, email: str, password: str) -> None:
    sql = "INSERT INTO users (users_name, users_email, users_password, clock_manager_id) VALUES "
    clock_id = createClock(srv_db)
    values = f"('{name}', '{email}', '{password}', {clock_id});"
    query = sql + values
    srv_db.execute_query(query)


def createUser(srv_db: SQLServer, name: str, email: str, password: str) -> int:
    sql = "INSERT INTO users (users_name, users_email, users_password, clock_manager_id) VALUES "
    clock_id = createClock(srv_db)
    values = f"('{name}', '{email}', '{password}', {clock_id});"
    query = sql + values
    return srv_db.execute_query_id(query)


def createProject(
        srv_db: SQLServer,
        name: str,
        version: str,
        description: Optional[str] = None
):
    requests = [
        "INSERT INTO LanAudacity(lan_audacity_name, start_version, last_version, lan_audacity_description, clock_manager_id) VALUES ",
        "INSERT INTO LanAudacity(lan_audacity_name, start_version, last_version, clock_manager_id) VALUES "
    ]
    clock_id = createClock(srv_db)
    if description:
        values = f"('{name}', '{version}', '{version}', '{
            description}', {clock_id});"
        query = requests[0] + values
    else:
        values = f"('{name}', '{version}', '{version}', {clock_id});"
        query = requests[1] + values

    srv_db.execute_query(query)


def addAuthorToProject(srv_db: SQLServer, project_id: int, user_id: int):
    sql = "INSERT INTO Authors (authors_id, project_id) VALUES "
    values = f"({user_id}, {project_id});"
    query = sql + values
    srv_db.execute_query(query)


def createWebAddress(
        srv_db: SQLServer,
        ipv4: Optional[str] = None,
        mask_ipv4: Optional[str] = None,
        ipv4_public: Optional[str] = None,
        cidr: Optional[str] = None,
        ipv6_local: Optional[str] = None,
        ipv6_global: Optional[str] = None
) -> int:
    # Vérifier si au moins une donnée est fournie
    if not any([ipv4, mask_ipv4, ipv4_public, cidr, ipv6_local, ipv6_global]):
        logging.error("Au moins un des paramètres doit être fourni.")
        raise ValueError("Au moins un des paramètres doit être fourni.")

    # Calculer CIDR si ipv4 et mask_ipv4 sont fournis
    if ipv4 and mask_ipv4 and not cidr:
        # Calcul du CIDR simplifié (assume un masque valide)
        mask_octets = map(int, mask_ipv4.split('.'))
        cidr_bits = sum(bin(octet).count('1') for octet in mask_octets)
        cidr = f"{ipv4}/{cidr_bits}"

    # Calculer ipv4 et mask_ipv4 si cidr est fourni
    if cidr and (not ipv4 or not mask_ipv4):
        try:
            ip, cidr_bits = cidr.split('/')
            cidr_bits = int(cidr_bits)
            ipv4 = ipv4 or ip
            mask_ipv4 = '.'.join(
                [str((0xffffffff << (32 - cidr_bits) >> i) & 0xff)
                 for i in (24, 16, 8, 0)]
            )
        except Exception as e:
            logging.error(f"Erreur lors de l'analyse du CIDR: {e}")
            raise ValueError(f"Erreur lors de l'analyse du CIDR: {e}")

    # Construire la requête INSERT en fonction des données disponibles
    columns = []
    values = []

    if ipv4:
        columns.append("ipv4")
        values.append(f"'{ipv4}'")
    if mask_ipv4:
        columns.append("mask_ipv4")
        values.append(f"'{mask_ipv4}'")
    if ipv4_public:
        columns.append("ipv4_public")
        values.append(f"'{ipv4_public}'")
    if cidr:
        columns.append("cidr")
        values.append(f"'{cidr}'")
    if ipv6_local:
        columns.append("ipv6_local")
        values.append(f"'{ipv6_local}'")
    if ipv6_global:
        columns.append("ipv6_global")
        values.append(f"'{ipv6_global}'")

    # Générer la requête
    columns_str = ", ".join(columns)
    values_str = ", ".join(values)
    query = f"INSERT INTO WebAddress ({columns_str}) VALUES ({values_str});"

    # Exécuter la requête et retourner l'identifiant inséré
    return srv_db.execute_query_id(query)


def createNetwork(
        srv_db: SQLServer,
        name: str,
        web_address_id: int,
        domain_name: Optional[str] = None
) -> None:
    request = [
        "INSERT INTO Network (uuid, name_object, web_address_id, domain_name, clock_manager_id) VALUES ",
        "INSERT INTO Network (uuid, name_object, web_address_id, clock_manager_id) VALUES "
    ]
    clock_id = createClock(srv_db)
    uuid_str = str(uuid.uuid4())

    if domain_name:
        values = f"('{uuid_str}', '{name}', {web_address_id}, '{
            domain_name}', {clock_id});"
        query = request[0] + values
    else:
        values = f"('{uuid_str}', '{name}', {web_address_id}, {clock_id});"
        query = request[1] + values

    srv_db.execute_query(query)


def createDevice(
        srv_db: SQLServer,
        name: str,
        web_address_id: int,
        device_type_id: int) -> int:
    sql = "INSERT INTO Device (uuid, name_object, web_address_id, device_type_id, clock_manager_id) VALUES "
    uuid_str = str(uuid.uuid4())
    clock_id = createClock(srv_db)

    values = f"('{uuid_str}', '{name}', {web_address_id}, {
        device_type_id}, {clock_id});"
    query = sql + values
    return srv_db.execute_query_id(query)


def createDeviceType(
        srv_db: SQLServer,
        name: str,
        osi_layer_id: int,
        pixmap_path: Optional[str] = None,
        category_description: Optional[str] = None
) -> None:
    # Construire la liste des colonnes et des valeurs
    columns = ["name_object", "osi_layer_id"]
    values = [f"'{name}'", osi_layer_id]

    if pixmap_path:
        columns.append("pixmap_path")
        values.append(f"'{pixmap_path}'")
    if category_description:
        columns.append("category_description")
        values.append(f"'{category_description}'")

    # Générer la requête SQL
    columns_str = ", ".join(columns)
    values_str = ", ".join(values)
    query = f"INSERT INTO DeviceType ({columns_str}) VALUES ({values_str});"

    # Exécuter la requête
    srv_db.execute_query(query)


def addDeviceToNetwork(srv_db: SQLServer, device_id: int, network_id: int):
    sql = "INSERT INTO NetworkDevice (device_id, network_id) VALUES "
    values = f"({device_id}, {network_id});"
    query = sql + values
    srv_db.execute_query(query)


def addNetworkToProject(srv_db: SQLServer, network_id: int, project_id: int):
    sql = "INSERT INTO ProjectNetwork (network_id, lan_audacity_id) VALUES "
    values = f"({network_id}, {project_id});"
    query = sql + values
    srv_db.execute_query(query)


def addOSAccuracyToDevice(srv_db: SQLServer, device_id: int, os_accuracy: int, name_os: str):
    sql = "INSERT INTO osaccuracy (device_id, accuracy_int, name_object) VALUES "
    values = f"({device_id}, {os_accuracy}, '{name_os}');"
    query = sql + values
    srv_db.execute_query(query)


def addPortsNewsToDevice(
        srv_db: SQLServer,
        device_id: int,
        port_number: int,
        protocol: Optional[str] = None,
        port_status: Optional[str] = None,
        port_service: Optional[str] = None,
        port_version: Optional[str] = None
) -> None:
    # Construire la liste des colonnes et des valeurs
    columns = ["device_id", "port_number"]
    values = [device_id, port_number]

    if protocol:
        columns.append("protocol")
        values.append(f"'{protocol}'")
    if port_status:
        columns.append("port_status")
        values.append(f"'{port_status}'")
    if port_service:
        columns.append("port_service")
        values.append(f"'{port_service}'")
    if port_version:
        columns.append("port_version")
        values.append(f"'{port_version}'")

    # Générer la requête SQL
    columns_str = ", ".join(columns)
    values_str = ", ".join(values)
    query = f"INSERT INTO DevicePorts ({columns_str}) VALUES ({values_str});"

    # Exécuter la requête
    srv_db.execute_query(query)


def addRoleToUser(srv_db: SQLServer, user_id: int, role_id: int):
    sql = "INSERT INTO User_Roles (user_id, role_id) VALUES "
    values = f"({user_id}, {role_id});"
    query = sql + values
    srv_db.execute_query(query)


# --- Récupération de données dans la base de données ---

# Getters All


def getAllProjects(srv_db: SQLServer) -> Any:
    return srv_db.fetch_data("SELECT * FROM LanAudacity;")


def getAllUsers(srv_db: SQLServer) -> Any:
    return srv_db.fetch_data("SELECT * FROM Users;")


def getAllDevices(srv_db: SQLServer) -> Any:
    return srv_db.fetch_data("SELECT * FROM Device;")


def getAllNetworks(srv_db: SQLServer) -> Any:
    return srv_db.fetch_data("SELECT * FROM Network;")


def getAllDeviceTypes(srv_db: SQLServer) -> Any:
    return srv_db.fetch_data("SELECT * FROM DeviceType;")


def getAllOSILayers(srv_db: SQLServer) -> Any:
    return srv_db.fetch_data("SELECT * FROM OSILayer;")

# Project Manager


def getProjectByName(srv_db: SQLServer, name: str) -> Any:
    return srv_db.fetch_data(f"SELECT * FROM LanAudacity WHERE lan_audacity_name = '{name}';")


def getProjectByAuthor(srv_db: SQLServer, author_name: str) -> Any:
    request = f"SELECT * FROM LanAudacity WHERE id IN (SELECT project_id FROM Authors WHERE authors_id IN (SELECT id FROM Users WHERE users_name = '{
        author_name}'));"
    return srv_db.fetch_data(request)


def getAuthorByProject(srv_db: SQLServer, project_name: str) -> Any:
    request = f"SELECT * FROM Users WHERE id IN (SELECT authors_id FROM Authors WHERE project_id IN (SELECT id FROM LanAudacity WHERE lan_audacity_name = '{
        project_name}'));"
    return srv_db.fetch_data(request)


def getNetworkByProject(srv_db: SQLServer, project_name: str) -> Any:
    request = f"SELECT * FROM Network WHERE id IN (SELECT network_id FROM ProjectNetwork WHERE lan_audacity_id IN (SELECT id FROM LanAudacity WHERE lan_audacity_name = '{
        project_name}'));"
    return srv_db.fetch_data(request)

# Network Manager


def getDeviceByNetwork(srv_db: SQLServer, network_name: str) -> Any:
    request = f"SELECT * FROM Device WHERE id IN (SELECT device_id FROM NetworkDevice WHERE network_id IN (SELECT id FROM Network WHERE name_object = '{
        network_name}'));"
    return srv_db.fetch_data(request)

# Device Manager


def getDeviceTypeByDevice(srv_db: SQLServer, device_name: str) -> Any:
    request = f"SELECT * FROM DeviceType WHERE id IN (SELECT device_type_id FROM Device WHERE name_object = '{
        device_name}');"
    return srv_db.fetch_data(request)

# DeviceType Manager


def getOSILayerByDeviceType(srv_db: SQLServer, device_type_name: str) -> Any:
    request = f"SELECT * FROM OSILayer WHERE id IN (SELECT osi_layer_id FROM DeviceType WHERE name_object = '{
        device_type_name}');"
    return srv_db.fetch_data(request)

# WebAddress Manager


def getWebAddressByNetwork(srv_db: SQLServer, network_name: str) -> Any:
    request = f"SELECT * FROM WebAddress WHERE id IN (SELECT web_address_id FROM Network WHERE name_object = '{
        network_name}');"
    return srv_db.fetch_data(request)

# ClockManager


def getClockByProject(srv_db: SQLServer, project_name: str) -> Any:
    request = f"SELECT * FROM ClockManager WHERE id IN (SELECT clock_manager_id FROM LanAudacity WHERE lan_audacity_name = '{
        project_name}');"
    return srv_db.fetch_data(request)


def getClockByDevice(srv_db: SQLServer, device_name: str) -> Any:
    request = f"SELECT * FROM ClockManager WHERE id IN (SELECT clock_manager_id FROM Device WHERE name_object = '{
        device_name}');"
    return srv_db.fetch_data(request)


def getClockByNetwork(srv_db: SQLServer, network_name: str) -> Any:
    request = f"SELECT * FROM ClockManager WHERE id IN (SELECT clock_manager_id FROM Network WHERE name_object = '{
        network_name}');"
    return srv_db.fetch_data(request)


def getClockByUser(srv_db: SQLServer, user_name: str) -> Any:
    request = f"SELECT * FROM ClockManager WHERE id IN (SELECT clock_manager_id FROM Users WHERE users_name = '{
        user_name}');"
    return srv_db.fetch_data(request)
