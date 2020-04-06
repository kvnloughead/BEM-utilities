#!usr/bin/python
"""
Program to speed up creation of BEM Nested style css directories.
Intended to run from within root directory of project.
Assumes user defined css within ./blocks directory.
"""

import shutil, os, sys

# TODO Create root directory 
def make_all_directories(blocks):
    """
    Calls on make_directories to walk through dictionary of BEM blocks
    and elements to create nested file structure.
    
    blocks is a dictionary: {block : [elements]}.  Enter elements without
    underscores, but include all underscores for modifiers (including leading) 
    """
    for block in blocks:
        # make block level directories and css files
        make_directories(block)
        make_css_files(block, block)
        for element in blocks[block]:
            # make element level directories
            if "_" not in element:
                make_directories(block, f"__{element}")
                make_css_files(f"{block}__{element}", block, f"__{element}")
            elif element.startswith("_"):
                # make block_modifier directories
                try:
                    elem, mod, val = element.split("_")
                    filename = f"{block}_{mod}_{val}"
                except ValueError:
                    elem, mod = element.split("_")
                    filename = f"{block}_{mod}"
                make_directories(block, f"_{mod}")
                make_css_files(filename, block, f"_{mod}")
            else: 
                # make block__element_modifier directories
                elem, mod, val = element.split("_")
                make_directories(block, f"__{elem}", f"_{mod}")
                make_css_files(f"{block}__{elem}_{mod}_{val}", block, f"__{elem}", f"_{mod}")

def make_directories(*path_parts):
    """Forms path blocks/path_parts and makes corresponding directory."""
    try:
        path = os.path.join('blocks', *path_parts)
        os.mkdir(path)
    except FileExistsError:
        pass

def make_css_files(filename, *path_parts):
    # make css files
    filename = f"{filename}.css"
    path = os.path.join("blocks", *path_parts, filename)
    print(path)
    with open(path, "w+") as f:
        selector = f".{filename}"[:-4]
        f.write(selector + " {\n\n}")


blocks = {  'root'   : [],
            'header' : ['logo', 'title', 'subtitle', '_theme_dark'],
            'footer' : ['logo', 'copyright', 'links'],
            'content': ['main-text', 'sidebar', 'sidebar_place_left', 'sidebar_place_right'],   
         }

make_all_directories(blocks)