import os

NEW_PROJECT: dict = {
    "window_title": "Setup Project",
    "title": "New Project",
    "separator": True,
    "fields": [
        {
            "label": "Project Name",
            "required": True,
            "input": {
                "type": "text",
                "name": "project_name",
                "placeholder": "Enter project name",
                "value": ""
            }
        },
        {
            "label": "Project Location",
            "required": True,
            "input": {
                "type": "folder",
                "name": "save_path",
                "placeholder": "Select project location",
                "dialog_title": "Choose project location",
                "value": os.path.expanduser("~"),
                "readonly": True
            }
        },
        {
            "label": "Author",
            "required": False,
            "input": {
                "type": "text",
                "name": "author",
                "placeholder": "Enter author name",
                "value": ""
            }
        }
    ]
}

DISCOVERY_MODE: dict = {
    "window_title": "Process Mode",
    "title": "Discovery Mode",
    "separator": True,
    "fields": [
        {
            "label": "Mode de fonctionnement",
            "input": {
                "type": "radio",
                "name": "auto_mode",
                "text": "Auto-mode: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "checked": True,
                "slot": lambda checked: print(f"Auto mode: {checked}")
            }
        },
        {
            "label": "",
            "input": {
                "type": "radio",
                "name": "manual_mode",
                "text": "Manual mode: ⚠️ Warning! This mode requires advanced knowledge.",
                "checked": False,
                "slot": lambda checked: print(f"Manual mode: {checked}")
            }
        }
    ]
}

NEW_LAN: dict = {
    "window_title": "Setup Network",
    "title": "New Network",
    "separator": True,
    "fields": [
        {
            "label": "Network Name",
            "required": False,
            "input": {
                "type": "text",
                "name": "network_name",
                "placeholder": "Enter network name",
                "value": ""
            }
        },
        {
            "label": "Network IPv4",
            "required": True,
            "input": {
                "type": "text",
                "name": "ipv4",
                "placeholder": "127.0.0.0",
                "value": "192.168.0.0"
            }
        },
        {
            "label": "Network Mask IPv4",
            "required": True,
            "input": {
                "type": "text",
                "name": "mask_ipv4",
                "placeholder": "255.0.0.0",
                "value": "255.255.255.0"
            }
        },
        {
            "label": "Network IPv6",
            "required": False,
            "input": {
                "type": "text",
                "name": "ipv6",
                "placeholder": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
                "value": ""
            }
        },
        {
            "label": "Network DNS",
            "required": False,
            "input": {
                "type": "text",
                "name": "dns",
                "placeholder": "127.0.0.0 or it-connect.fr",
                "value": ""
            }
        }
    ]
}

NEW_UC: dict = {
    "window_title": "Setup UC",
    "title": "New UC",
    "separator": True,
    "fields": [
        {
            "label": "UC Name",
            "required": False,
            "input": {
                "type": "text",
                "name": "uc_name",
                "placeholder": "Enter UC name",
                "value": ""
            }
        },
        {
            "label": "UC IPv4",
            "required": True,
            "input": {
                "type": "text",
                "name": "ipv4",
                "placeholder": "127.0.0.1",
                "value": ""
            }
        },
        {
            "label": "UC Mask IPv4",
            "required": True,
            "input": {
                "type": "text",
                "name": "mask_ipv4",
                "placeholder": "255.0.0.0",
                "value": ""
            }
        },
        {
            "label": "UC IPv6",
            "required": False,
            "input": {
                "type": "text",
                "name": "ipv6",
                "placeholder": "::1",
                "value": ""
            }
        },
        {
            "label": "UC Type",
            "required": False,
            "input": {
                "type": "combo",
                "name": "uc_type",
                "value": "Terminal User",
                "options": [
                    {"label": "Terminal User", "value": "Terminal User"},
                    {"label": "Router", "value": "Router"},
                    {"label": "Switch", "value": "Switch"},
                    {"label": "Firewall", "value": "Firewall"},
                    {"label": "Gateway", "value": "Gateway"},
                    {"label": "Server", "value": "Server"}
                ]
            }
        },
        {
            "label": "UC Model",
            "required": False,
            "input": {
                "type": "text",
                "name": "uc_model",
                "placeholder": "Enter UC model, ex: 881, 2960, 5505, etc.",
                "value": ""
            }
        },
        {
            "label": "UC Brand",
            "required": False,
            "input": {
                "type": "text",
                "name": "uc_brand",
                "placeholder": "Enter UC brand, ex: Cisco, HP, Dell, etc.",
                "value": ""
            }
        },
        {
            "label": "UC MAC Address",
            "required": False,
            "input": {
                "type": "text",
                "name": "uc_mac",
                "placeholder": "Enter UC MAC address, ex: 00:00:00:00:00:00",
                "value": ""
            }
        }
    ]
}

NEW_FILE: dict = {
    "window_title": "Setup Explorer",
    "title": "New File",
    "separator": True,
    "fields": [
        {
            "input": {
                "type": "text",
                "placeholder": "new_file.txt",
                "name": "filename",
                "value": ""
            },
            "label": "Nom du fichier:",
            "required": True
        },
        {
            "input": {
                "type": "hidden",
                "name": "parent_path",
                "value": ""
            }
        }
    ]
}

NEW_FOLDER: dict = {
    "window_title": "Setup Explorer",
    "title": "New Folder",
    "separator": True,
    "fields": [
        {
            "label": "Nom du dossier:",
            "required": True,
            "input": {
                "type": "text",
                "name": "foldername",
                "placeholder": "nouveau_dossier.d",
                "value": ""
            }
        },
        {
            "input": {
                "type": "hidden",
                "name": "parent_path",
                "value": ""
            }
        }
    ]
}
