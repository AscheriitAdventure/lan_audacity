# from lan_test3 import LanAudacity
import os


files = os.listdir(os.getcwd())
path_project = os.path.join(os.getcwd(), files[8])
print(path_project)
