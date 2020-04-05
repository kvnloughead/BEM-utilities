#!usr/bin/python
"""
Program to speed up creation of BEM Nested style css directories.
Intended to run from within root directory of project.
Assumes user defined css within ./blocks directory.
"""

import shutil, os, sys

def make_directories(blocks):
    """blocks is a dictionary: {block : [elements]}"""
    for block in blocks:
        # make block level directories
        path = os.path.join('blocks', block)
        os.mkdir(path)
        # make element level directories
        for element in blocks[block]:
            if "_" not in element:
                path = os.path.join('blocks', block, element)
                os.mkdir(path)
            # make block_modifier directories
            elif element.startswith("_"):
                mod = element.split("_")[1]
                path = os.path.join('blocks', block, f"_{mod}")
                os.mkdir(path)
            # make block__element_modifier directories
            else:
                block, mod, val = element.split("")



blocks = {
            'header' : ['logo', 'title', 'subtitle', '_theme_dark'],
            'footer' : ['logo', 'copyright', 'links'],
            'content': ['main-text', 'sidebar', 'sidebar_place_left', 'sidebar_place_right'],   
         }

make_directories(blocks)

