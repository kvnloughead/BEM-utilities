#!usr/bin/python
"""
This program 

  1. recieves the block/elem/mod/val data structure computed in parse_blocks.py
  2. uses that data to create nested BEM file structure
  3. calls functions from write.py to write 
      a. import statements to index and block.css files
  # TODO
      b. rewrite css selectors to the appropriate files  

"""

import os
import parse_blocks
import write

data = parse_blocks.gather_data('./blocks')

def build_file_structure(data):
  for block in data:

    write.import_to_index_css(block)

    elems_and_mods = data[block]
    if elems_and_mods:
      for elem_or_mod in elems_and_mods:
        if elem_or_mod.startswith('__'):
          build_elem_file_structure(block, elem_or_mod, data)
        else:
          build_mod_file_structure(block, elem_or_mod, data, isBlock=True)

def build_elem_file_structure(block, elem, data):
  elem_path = os.path.join(f'./blocks/{block}/{elem}/{block}{elem}.css')
  os.makedirs(os.path.dirname(elem_path), exist_ok=True)

  write.import_to_block_css(block, elem)
  # TODO write all selectors to block__elem.css
  
  mods = data[block][elem]
  if mods:
    for mod in mods:
      build_mod_file_structure(f'{block}/{elem}', mod, data, False, elem_path) 


def build_mod_file_structure(block, mod, data, isBlock=True, path=''):
  """
  isBlock - boolean indicated whether mod modifies block or element
  """
  mod_dirpath = os.path.join(f'./blocks/{block}/{mod}')
  os.makedirs(mod_dirpath, exist_ok=True)

  if not isBlock:
    block, elem = block.split('/')
    vals = data[block][elem][mod]
    if not vals:
      write.import_to_block_css(block, elem, mod)
      # TODO write css to block__elem_mod.css
      with open(os.path.join(mod_dirpath, f'{block}{elem}{mod}.css'), "w") as f:
        f.write(f'selectors for {block}{elem}{mod} go in here')

    else:
      for val in data[block][elem][mod]:
        write.import_to_block_css(block, elem, mod, val)
        with open(os.path.join(mod_dirpath, f'{block}{elem}{mod}{val}.css'), "w") as f:
          # TODO write css to block__elem_mod_val.css
          f.write(f'selectors for {block}{elem}{mod}{val} go in here')
          
  else:
    vals = data[block][mod]
    write.import_to_block_css(block, mod)

    if not vals:
      with open(os.path.join(mod_dirpath, f'{block}{mod}.css'), "w") as f:
        f.write(f'selectors for {block}{mod} go in here')
        
    else:
      for val in data[block][mod]:
        with open(os.path.join(mod_dirpath, f'{block}{mod}{val}.css'), "w") as f:
          f.write(f'selectors for {block}{mod}{val} go in here')



build_file_structure(data)