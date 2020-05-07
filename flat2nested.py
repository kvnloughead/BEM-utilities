#!usr/bin/python
"""
Program to facilitate changing from a flat BEM css structure to a 
nested structure.   

Requirements:

pages/index.css  (for the block level import statements)
blocks/          (directory containing all block level directories)
    page/
      page.css
    block-1/
      block-1.css
    block-2/
      block-2.css
    ...

Inside each block.css file are all declarations pertaining to that
block and its elements.
"""

import os
import sys

def gather_data(block_dir):
  """
  Gathers all necessary information into a dict with the following
  structure:

    data = {
      block: {

          elements:  [(elem_1, {mod: vals for mod of elem_1} , 
                      elem_2, {mod: vals for mod of elem_2}...],

          block_mods: {mod: vals for mod of block}

              }
            }
  """
  data = {}
  blocks = os.listdir(block_dir)
  get_elements_and_modifiers(blocks)
  

def get_elements_and_modifiers(blocks):
  """
  Reads each block level css file and gather elements,
  modifiers and values.
  """
  for block in blocks:
    block_path = os.path.join(f'blocks/{block}', f'{block}.css')
    with open(block_path, 'w+') as f:
      parse_css(f)

def parse_css(f):
  print('hi')

gather_data('./blocks')



