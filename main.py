#!usr/bin/python
"""
Program to speed up creation of BEM Nested style css directories.
Intended to run from within root directory of project.
Assumes user defined css within ./blocks directory.
"""

import shutil, os, sys

def make_all_directories(blocks):
    """
    Calls on make_directories to walk through dictionary of BEM blocks
    and elements to create nested file structure.
    
    blocks is a dictionary: {block : [elements]}.  Enter elements without
    underscores, but include all underscores for modifiers (including leading) 
    """
    for block in blocks:
        # make block level directories
        path = os.path.join('blocks', block)
        os.mkdir(path)
        # make element level directories
        for element in blocks[block]:
            if "_" not in element:
                make_directories(block, f"__{element}")
            elif element.startswith("_"):
                # make block_modifier directories
                mod = element.split("_")[1]
                make_directories(block, f"_{mod}")
            else: 
                # make block__element_modifier directories
                elem, mod, val = element.split("_")
                make_directories(block, f"__{elem}", f"_{mod}")

def make_directories(*path_parts):
    """Forms path blocks/path_parts and makes corresponding directory."""
    try:
        path = os.path.join('blocks', *path_parts)
        os.mkdir(path)
    except FileExistsError:
        pass

blocks = {
            'header' : ['logo', 'title', 'subtitle', '_theme_dark'],
            'footer' : ['logo', 'copyright', 'links'],
            'content': ['main-text', 'sidebar', 'sidebar_place_left', 'sidebar_place_right'],   
         }

make_all_directories(blocks)