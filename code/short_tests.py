import os.path

from src.classes.configurationFile import ConfigurationFile
from src.functionsExt import current_dir

softwareManager = ConfigurationFile(os.path.join(current_dir(), "conf", "config_app.yaml"))
print(softwareManager.get_extension(softwareManager.abs_path)+"_read")
# print(softwareManager.data['software'])
