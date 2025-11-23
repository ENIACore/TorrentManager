from os import walk
from pathlib import Path
from struct.node import Node

class Parser:
    def __init__(self) -> None:
        pass

    def process_nodes(self, path: Path) -> Node | None:
            
        for dirpath, dirnames, filenames in walk(path):
            print(f"Directory: {dirpath}")
            print(f"Subdirs: {dirnames}")
            print(f"Files: {filenames}")
