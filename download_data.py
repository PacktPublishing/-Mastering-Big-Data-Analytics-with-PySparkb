from pathlib import Path
import configparser
import os
import urllib3
from zipfile import ZipFile

# CONFIGURATIONS / SET UP
# Extract download path for Data Sets
DATA_SETS_PATH = Path(__file__).resolve().parent / "data-sets"
# Set chunk size for downloading (avoid unnecessary loading to memory)
CHUNK_SIZE = 1024 * 1024  # in bytes
# Name/location of the data_sets configuration file
CONFIG_LOCATION = Path(__file__).resolve().parent / "conf" / "data_sets.conf"

# TODO: add check mechanism for seeing if data was already downloaded. No need to re-download data that is already there

# Create data-sets folder if it does not yet exist
if not os.path.exists(DATA_SETS_PATH):
    print("Creating data-sets directory\n")
    os.makedirs(DATA_SETS_PATH)

# PROCESSING DATA SETS DEFINED IN CONFIGURATION FILE
config = configparser.ConfigParser()
config.read(CONFIG_LOCATION)

for section in config.sections():
    print("Processing {}".format(section))
    readme_md = None

    # Parse configuration for data_set
    data_set_config = config[section]
    download_path = data_set_config["download_path"]
    filename = data_set_config["filename"]
    has_readme = data_set_config.get("has_readme") == "True"
    destination_path = data_set_config.get("destination_path")
    if not has_readme:
        readme_location = data_set_config["readme_location"]
        license_info = data_set_config["license_info"]
        readme_md = "readme_location: {readme_location}\nlicense_info: {license_info}".format(
            readme_location=readme_location, license_info=license_info
        )

    # Set download location
    if destination_path:
        destination_path = DATA_SETS_PATH / destination_path
    else:
        destination_path = DATA_SETS_PATH

    if not os.path.exists(destination_path):
        print(" - Creating output directory")
        os.makedirs(destination_path)

    destination_filepath = str(destination_path / filename)

    # Create README.MD file (if needed)
    if readme_md:
        readme_loc = str(destination_path / "README.md")
        with open(readme_loc, "wb") as readme:
            print(" - Creating README.md file")
            readme.write(readme_md.encode("UTF-8"))

    # Download file using urllib3
    http = urllib3.PoolManager()
    r = http.request("GET", str(download_path), preload_content=False)
    with open(destination_filepath, "wb") as dest:
        print(' - Downloading "{}" to "{}"'.format(filename, destination_path))
        while True:
            data = r.read(CHUNK_SIZE)
            print(os.path.getsize(destination_path) / 1024, "KB downloaded!", end="\r")
            if not data:
                print(" - Finished downloading {}".format(filename))
                break
            dest.write(data)
    r.release_conn()

    # Extract zipfile
    print(' - Extracting "{}"'.format(filename))
    with ZipFile(destination_filepath, "r") as downloaded_file:
        downloaded_file.extractall(destination_path)

    # Remove zip file
    print(' - Removing zip-file "{}"'.format(filename))
    os.remove(destination_filepath)
