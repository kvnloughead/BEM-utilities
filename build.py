#!usr/bin/python
"""
This program recieves the block/elem/mod/val data structure
computed in parse_blocks.py and...
"""

import os
import parse_blocks
import read_and_write_css as rw

data = parse_blocks.gather_data('./blocks')

def build_file_structure(data):
  for block in data:
    for elem_or_mod in data[block]:
      if elem_or_mod.startswith('__'):
        build_elem_file_structure(block, elem_or_mod, data)
      else:
        build_mod_file_structure(block, elem_or_mod, data, True)

def build_elem_file_structure(block, elem, data):
  elem_path = os.path.join(f'./blocks/{block}/{elem}/{block}{elem}.css')
  os.makedirs(os.path.dirname(elem_path), exist_ok=True)
  with open(elem_path, "w") as f:
    f.write(f'selectors for {elem} go in here')
  
  mods = data[block][elem]
  if mods:
    for mod in mods:
      build_mod_file_structure(f'{block}/{elem}', mod, data, False) 

def build_mod_file_structure(block, mod, data, isBlock=True):
  """
  isBlock - boolean indicated whether mod modifies block or element
  """
  mod_dirpath = os.path.join(f'./blocks/{block}/{mod}')
  os.makedirs(mod_dirpath, exist_ok=True)

  if not isBlock:
    block, elem = block.split('/')
    if not data[block][elem][mod]:
      with open(os.path.join(mod_dirpath, f'{block}{elem}{mod}.css'), "w") as f:
        # TODO write css to these files
        f.write(f'selectors for {block}{elem}{mod} go in here')
    else:
      for val in data[block][elem][mod]:
        with open(os.path.join(mod_dirpath, f'{block}{elem}{mod}{val}.css'), "w") as f:
          # TODO write css to these files
          f.write(f'selectors for {block}{elem}{mod}{val} go in here')
  else:
    if not data[block][mod]:
      with open(os.path.join(mod_dirpath, f'{block}{mod}.css'), "w") as f:
        f.write(f'selectors for {block}{mod} go in here')
    else:
      for val in data[block][mod]:
        with open(os.path.join(mod_dirpath, f'{block}{mod}{val}.css'), "w") as f:
          f.write(f'selectors for {block}{mod}{val} go in here')


# build_file_structure(data)