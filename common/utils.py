"""
Some utility functions for data processing.
"""

from pathlib import Path
import os

# list folders in a folder
def list_folders(path: Path):
    return [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]


# list files in a folder
def list_files(path: Path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f != '.DS_Store']
