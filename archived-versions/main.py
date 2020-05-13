#!usr/bin/python
"""
Program to speed up creation of BEM Nested style css directories.
Intended to run from within root directory of project, with blocks/ and pages/index.css already in place.

Assumes user defined css is within ./../blocks directory.
Assumes main html file is named index.html, and only populates page level imports in pages/index.css.
"""

import os
import sys


# TODO make this into a command line utility

def make_all_directories(blocks):
    """
    Calls on make_directories to walk through dictionary of BEM blocks
    and elements to create nested file structure.
    
    blocks is a dictionary: {block : [elements]}.  Enter elements without
    underscores, but include all underscores for modifiers (including leading) 
    """
    
    block_imports = ""
    element_imports = {}
    for block in blocks:
        element_imports[block] = ""
        # make block level directories and css files
        make_directory(block)
        path = make_css_file(block, block)
        block_imports += write_import_statement(path)
        for element in blocks[block]:
            # make element level directories
            if "_" not in element:
                make_directory(block, f"__{element}")
                path = make_css_file(f"{block}__{element}", block, f"__{element}")
                path_to_import = f"./../__{element}/{block}__{element}.css"
            elif element.startswith("_"):
                # make block_modifier directories
                try:
                    elem, mod, val = element.split("_")
                    filename = f"{block}_{mod}_{val}"
                except ValueError:
                    elem, mod = element.split("_")
                    filename = f"{block}_{mod}"
                make_directory(block, f"_{mod}")
                path = make_css_file(filename, block, f"_{mod}")
                path_to_import = f"./../_{mod}/{block}_{mod}_{val}.css"
            else: 
                # make block__element_modifier directories
                elem, mod, val = element.split("_")
                make_directory(block, f"__{elem}", f"_{mod}")
                path = make_css_file(f"{block}__{elem}_{mod}_{val}", block, f"__{elem}", f"_{mod}")
                path_to_import = f"./../__{elem}/{block}__{elem}_{mod}_{val}.css"
            path_to_block = os.path.join("blocks", block, block + ".css")
            element_imports[block] += write_import_statement(path_to_import)
        try:
            line_prepender(path_to_block, element_imports[block])
        except UnboundLocalError:
            pass
    # write import statements to files
    
    line_prepender("pages/index.css", block_imports)
    
            

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

def write_import_statement(path_down):
    """
    path_up   - path to file in which to write import statements
    path_down - path to file to be imported
    """
    return f"@import url({path_down});\n"
    

def line_prepender(filename, line):
    """Prepends line to filename by creating a new file. Thanks to Stack 
    Overflow.  Single newline between line and original content."""
    with open(filename, "r+") as f:
        content = f.read()
        f.seek(0, 0)        
        f.write(line + "\n" + content)



blocks = {  'root'   : [],
            'header' : ['logo', 'title', 'subtitle', '_theme_dark'],
            'footer' : ['logo', 'copyright', 'links'],
            'content': ['main-text', 'sidebar', 'sidebar_place_left', 'sidebar_place_right'],   
         }

make_all_directories(blocks)