import os

VAR_TEST = "C:\\Users\\g.tronche\\Documents\\test_app\\Eyrein Network\\db\\interfaces\\4a895f3a-91c8-440d-98be-b473f87a7e66.json"
"""VAR_TEST = os.path.dirname(VAR_TEST)
VAR_TEST = os.path.dirname(VAR_TEST)
VAR_TEST = os.path.join(VAR_TEST, "desktop")

print(VAR_TEST)"""

VAR_TEST = os.path.join(os.path.dirname(os.path.dirname(VAR_TEST)), "desktop")
print(VAR_TEST)