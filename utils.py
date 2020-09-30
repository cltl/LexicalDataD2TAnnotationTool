import os
import shutil


def remove_and_create_folder(fldr):
    """
    Remove a folder, if existing, and re-create it.
    """
    if  os.path.exists(fldr):
        shutil.rmtree(fldr)
    os.mkdir(fldr)