import os
from _src._mdl.mdl_itm import IconItem, KeyboardItem, SoftwareParameters, Device, TextTranslate
import qtawesome as qta


class KeyboardManager:
    def __init__(self):
        self.__list_keyboard: list[KeyboardItem] = []

    @property
    def listKeyboard(self):
        return self.__list_keyboard

    def add_keyboard(self, keyboard: KeyboardItem):
        self.__list_keyboard.append(keyboard)

    def len_ls(self) -> int:
        return len(self.listKeyboard)


class IconsManager:
    def __init__(self):
        self.__list_icons: list[IconItem] = []
        self.set_default_icons()
        self.set_os_icon()

    @property
    def listIcons(self):
        return self.__list_icons

    def add_icons(self, icon: IconItem):
        self.__list_icons.append(icon)

    def len_ls(self) -> int:
        return len(self.listIcons)

    def set_default_icons(self):
        os_icon_ls = [
            (qta.icon("fa5s.globe", "fa5s.user-shield", options=[{"color": "blue"}, {"scale_factor": 0.75, "color": "silver"}]), "window_icon"),
            (qta.icon("fa5s.cloud", "fa5s.network-wired", options=[{"scale_factor": 1, "color": "blue"}, {"scale_factor": 0.75, "color": "white"}]), "netscan_icon"),
            (qta.icon("fa5s.sign-out-alt"), "exit_icon"),
            (qta.icon("fa5s.cog"), "settings_icon"),
            (qta.icon("fa5s.terminal"), "console_icon"),
            (qta.icon("fa5s.terminal", "fa5s.slash"), "hide_console_icon"),
            (qta.icon("fa5s.play", color="green"), "run_icon"),
            (qta.icon("fa5s.plus", color="blue"), "add_icon"),
            (qta.icon("fa5s.minus", color="red"), "minus_icon"),
            (qta.icon("fa5s.filter", color="grey"), "sort_icon"),
            (qta.icon("fa5s.map", "fa5s.map-signs", options=[{"scale_factor": 1, "color": "grey"}, {"scale_factor": 0.85, "color": "green"}]), "map_icon"),
            (qta.icon("fa5s.desktop", "fa5s.question", options=[{"scale_factor": 1, "color": "grey"}, {"scale_factor": 0.85, "color": "blue"}]), "uc-question-mark_icon"),
            (qta.icon("fa5s.exchange-alt", color="RoyalBlue"), "extend_icon"),
            (qta.icon("fa5s.tools", color="SlateGray"), "tools_icon"),
            (qta.icon("fa5s.keyboard", color="DarkGray"), "key_short_icon"),
            (qta.icon("fa5s.icons", color="MediumPurple"), "ico_icon"),
            (qta.icon("fa5s.window-maximize", "fa5s.shapes", options=[{"color": "DarkGray"}, {"scale_factor": 0.75, "color": "ForestGreen"}]), "th_wind_icon"),
            (qta.icon('fa5s.paint-brush', color='Grey'), 'Edit'),
            (qta.icon('fa5s.map-marked-alt', color='SaddleBrown'), 'map_device'),
            (qta.icon('fa5s.info-circle', color='Orange'), 'info_device')
        ]

        for icon, flag in os_icon_ls:
            self.add_icons(IconItem(icon, flag))

    def set_os_icon(self):
        os_icon_ls = [
            (qta.icon('fa5b.linux'), 'linux_os'),
            (qta.icon('fa5b.ubuntu', color='DarkOrange'), 'ubuntu_os'),
            (qta.icon('fa5b.suse', color='MediumSeaGreen'), 'suse_os'),
            (qta.icon('fa5b.redhat', color='Red'), 'redhat_os'),
            (qta.icon('fa5b.fedora', color='Navy'), 'fedora_os'),
            (qta.icon('fa5b.centos', color='DarkOrchid'), 'centos_os'),
            (qta.icon('fa5b.windows', color='SteelBlue'), 'windows_os'),
            (qta.icon('fa5b.android', color='ForestGreen'), 'android_os'),
            (qta.icon('fa5b.apple', color='Ivory'), 'darwin_os'),
            (qta.icon('fa5b.apple', color='Ivory'), 'ios_os'),
            # (qta.icon('fa5b.debian', color='Purple'), 'debian_os'),
        ]
        for icon, flag in os_icon_ls:
            self.add_icons(IconItem(icon, flag))

    def get_cidr(self):
        print('rr')

class SettingsModel:
    def __init__(self):
        self.__keyboards = KeyboardManager()
        self.__icons = IconsManager()
        self.__infos_app = SoftwareParameters()
        self.__window_style = None
        self.setDefaultKeyboard()

    @property
    def keyboard(self):
        return self.__keyboards

    @property
    def icons(self):
        return self.__icons

    @property
    def infoApp(self):
        return self.__infos_app

    @property
    def windowStyle(self):
        return self.__window_style

    @staticmethod
    def set_path() -> str:
        return os.getcwd()

    def get_1_icon(self, label: str) -> IconItem:
        if label and self.icons.len_ls() > 0:
            for icon in self.icons.listIcons:
                if icon.label == label:
                    return icon
        pass

    def get_1_keyboard(self, label: str) -> KeyboardItem:
        if label and self.keyboard.len_ls() > 0:
            for key in self.keyboard.listKeyboard:
                if key.nameAction == label:
                    return key
        pass

    def setDefaultKeyboard(self):
        key0 = KeyboardItem(
            "New Scan", "Alt+S", self.get_1_icon("netscan_icon").objIcon
        )
        self.keyboard.add_keyboard(key0)
        key1 = KeyboardItem("&Exit", "Alt+F4", self.get_1_icon("exit_icon").objIcon)
        self.keyboard.add_keyboard(key1)
        key2 = KeyboardItem("Home", "Ctrl+L", self.get_1_icon("window_icon").objIcon)
        self.keyboard.add_keyboard(key2)
        key3 = KeyboardItem(
            "Params", "Ctrl+,", self.get_1_icon("settings_icon").objIcon
        )
        self.keyboard.add_keyboard(key3)
        key4 = KeyboardItem(
            "New Terminal", "Ctrl+Alt+B", self.get_1_icon("console_icon").objIcon
        )
        self.keyboard.add_keyboard(key4)
        key5 = KeyboardItem(
            "Hide Terminal", "Ctrl+Alt+H", self.get_1_icon("hide_console_icon").objIcon
        )
        self.keyboard.add_keyboard(key5)
        key6 = KeyboardItem("Show Tree View", "Ctrl+Alt+T")
        self.keyboard.add_keyboard(key6)


class DeviceManager:
    def __init__(self):
        self.__device_list: list[Device] = []

    @property
    def device_list(self):
        return self.__device_list

    def add_device(self, device: Device):
        self.device_list.append(device)

    def remove_device(self, device: Device):
        if device in self.device_list:
            self.device_list.remove(device)

    def len_device(self) -> int:
        return len(self.device_list)

    def __str__(self) -> str:
        return f"DeviceManager: {self.len_device()} devices"


class TextTranslateManager:
    def __init__(self):
        self.__txt_translate_list: list[TextTranslate] = []
        self.__language_choice: str = 'English'
        self.language_ls: list[TextTranslate] = []
        self.set_default()

    @property
    def txt_translate_ls(self):
        return self.__txt_translate_list
    @property
    def languageChoice(self):
        return self.__language_choice

    @languageChoice.setter
    def languageChoice(self, var: str):
        if var:
            self.__language_choice = var

    def add_translate(self, txt: TextTranslate):
        self.__txt_translate_list.append(txt)

    def remove_translate(self, txt: TextTranslate):
        if txt in self.txt_translate_ls:
            self.txt_translate_ls.remove(txt)

    def len_translate(self):
        return len(self.txt_translate_ls)

    def get_langue(self) -> list[str]:
        lang_set = set()
        for translate in self.txt_translate_ls:
            lang_set.add(translate.referenceLangue)
        lang_list = sorted(list(lang_set))

        return lang_list

    def get_txt(self, lbl: str) -> TextTranslate:
        for translate in self.txt_translate_ls:
            if translate.referenceExpression == lbl and translate.referenceLangue == self.languageChoice:
                return translate
        pass

    def set_default(self):
        translation_pairs = [
            ('English', '&File', '&File'),
            ('Français', '&File', '&Fichier'),
            ('English', '&Edit', '&Edit'),
            ('Français', '&Edit', '&Modifier'),
            ('English', '&Exit', '&Exit'),
            ('Français', '&Exit', '&Quitter'),
            ('English', '&View', '&View'),
            ('Français', '&View', '&Afficher'),
            ('English', '&Help', '&Help'),
            ('Français', '&Help', '&Aide'),
            ('English', '&Settings', '&Settings'),
            ('Français', '&Settings', '&Paramètres'),
            ('English', 'Settings', 'Settings'),
            ('Français', 'Settings', 'Paramètres'),
            ('English', '&Terminal', '&Terminal'),
            ('Français', '&Terminal', '&Console'),
            ('English', 'Terminal', 'Terminal'),
            ('Français', 'Terminal', 'Console'),
            ('English', 'Net Explorer', 'Net Explorer'),
            ('Français', 'Net Explorer', 'Réseaux LAN/WAN'),
            ('English', 'Extends', 'Extends'),
            ('Français', 'Extends', 'Étendre'),
            ('English', 'Application Settings', 'Application Settings'),
            ('Français', 'Application Settings', 'Paramètres Application'),
            ('English', 'Keyboard Shortcut', 'Keyboard Shortcut'),
            ('Français', 'Keyboard Shortcut', 'Raccourci Clavier'),
            ('English', 'Icons Settings', 'Icons Settings'),
            ('Français', 'Icons Settings', 'Paramètres Icons'),
            ('English', 'Window Settings', 'Window Settings'),
            ('Français', 'Window Settings', 'Paramètres de la Fenêtre'),
            ('English', 'Hide Terminal', 'Hide Terminal'),
            ('Français', 'Hide Terminal', 'Cacher la Console'),
            ('English', 'New Terminal', 'New Terminal'),
            ('Français', 'New Terminal', 'Nouvelle Console'),
            ('English', 'Home', 'Home'),
            ('Français', 'Home', 'Accueil'),
            ('English', 'Params', 'Settings'),
            ('Français', 'Params', 'Paramètres'),
            ('English', 'Show Tree View', 'Show Net Explorer'),
            ('Français', 'Show Tree View', 'Afficher Réseaux'),
            ('English', 'New Scan', 'New Network'),
            ('Français', 'New Scan', 'Nouveau Réseaux'),
            ('English', 'Info Device', 'Info Device'),
            ('Français', 'Info Device', 'Informations\nMatériel Informatique'),
            ('English', 'Map Device', 'Map Device'),
            ('Français', 'Map Device', 'Carte Réseaux'),
        ]

        # Ajouter chaque paire de traduction à la liste
        for lang, key, value in translation_pairs:
            self.add_translate(TextTranslate(lang, key, value))
