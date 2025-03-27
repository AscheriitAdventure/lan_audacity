from src.utils import *
import os

if __name__ == '__main__':
    tmpd: dict = {
        "app_path": os.getcwd(),
        "debug": False
    }
    scan_app = ScanApp(**tmpd)
    scan_app.generateEnvironment()
