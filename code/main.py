from src.classes.cl_app_sys import OsSys
import platform
import sys, logging, os

# Create an instance of the OsSys class
os_sys = OsSys(platform.system(), platform.version())

# Execute the operating system
if os_sys.exec_os():
    # Execute the software scan
    if os_sys.exec_software() > 0:
        logging.warning("Some software is missing.")
        sys.exit(1)
    else:
        # launch the docker-compose file
        os.system("docker-compose up -d")
else:
    logging.info("Operating system not supported.")
    sys.exit(1)