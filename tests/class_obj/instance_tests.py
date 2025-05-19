import os

tmp_d = dict()
tmp_d["app_path"] = os.getcwd()
tmp_d["debug"] = False
tmp_d["tests_list"] = [
    "tests/class_obj/instance_tests.py",
    "tests/class_obj/class_tests.py",
    "tests/class_obj/scan_tests.py",
    "tests/class_obj/scan_tests2.py",
    "tests/class_obj/scan_tests3.py",
]

if __name__ == "__main__":
    if isinstance(tmp_d, dict):
        print(f"tmp_d is a dictionary")
        
    if isinstance(tmp_d.get("app_path"), str):
        print(f"app_path is a string")
    
    if isinstance(tmp_d.get("debug"), bool):
        print(f"debug is a boolean")
    
    if isinstance(tmp_d.get("tests_list"), list):
        print(f"tests_list is a list")
