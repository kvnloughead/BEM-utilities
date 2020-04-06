#!usr/bin/python
"""
Program to speed up creation of BEM Nested style css directories.
Intended to run from within root directory of project, with blocks and pages directories already in place.

Assumes user defined css is within ./blocks directory.
Assumes main html file is named index.html, and only populates page level imports in pages/index.css.
"""

import os

# TODO make this into a command line utility
# TODO write a bash script or alias to simplify opening BEM css files within vscode

# TODO add in importing statements

def make_all_directories(blocks):
    """
    Calls on make_directories to walk through dictionary of BEM blocks
    and elements to create nested file structure.
    
    blocks is a dictionary: {block : [elements]}.  Enter elements without
    underscores, but include all underscores for modifiers (including leading) 
    """ 
    for block in blocks:
        # make block level directories and css files
        make_directory(block)
        path_down = make_css_file(block, block)
        path_up = os.path.join("pages", "index.css")
        add_import_statements(path_up, path_down)
        for element in blocks[block]:
            # make element level directories
            if "_" not in element:
                make_directory(block, f"__{element}")
                path_down = make_css_file(f"{block}__{element}", block, f"__{element}")
            elif element.startswith("_"):
                # make block_modifier directories
                try:
                    elem, mod, val = element.split("_")
                    filename = f"{block}_{mod}_{val}"
                except ValueError:
                    elem, mod = element.split("_")
                    filename = f"{block}_{mod}"
                make_directory(block, f"_{mod}")
                path_down = make_css_file(filename, block, f"_{mod}")
            else: 
                # make block__element_modifier directories
                elem, mod, val = element.split("_")
                make_directory(block, f"__{elem}", f"_{mod}")
                path_down = make_css_file(f"{block}__{elem}_{mod}_{val}", block, f"__{elem}", f"_{mod}")
            path_up = os.path.join("blocks", block, block + ".css")
            add_import_statements(path_up, path_down)

def make_directory(*path_parts):
    """Forms path blocks/path_parts and makes corresponding directory."""
    try:
        path = os.path.join('blocks', *path_parts)
        os.mkdir(path)
    except FileExistsError:
        pass

def make_css_file(filename, *path_parts):
    """Creates path_parts/filename.css in the appropriate folder."""
    path = os.path.join("blocks", *path_parts, filename + ".css")
    with open(path, "w+") as f:
        selector = f".{filename}"
        f.write(selector + " {\n\n}")
    return path

def add_import_statements(path_up, path_down):
    """
    path_up   - path to file in which to write import statements
    path_down - path to file to be imported
    """
    print(path_up, path_down)
    with open(path_up, "a+") as f:
        f.write(f"@import url(../{path_down});\n")



blocks = {  'root'   : [],
            'header' : ['logo', 'title', 'subtitle', '_theme_dark'],
            'footer' : ['logo', 'copyright', 'links'],
            'content': ['main-text', 'sidebar', 'sidebar_place_left', 'sidebar_place_right'],   
         }

make_all_directories(blocks)