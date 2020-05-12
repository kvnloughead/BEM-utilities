#!usr/bin/python
"""
This program 

  1. recieves the block/elem/mod/val data structure computed in parse_blocks.py
  2. uses that data to create nested BEM file structure
  3. calls functions from write.py to write 
      a. import statements to index and block.css files
      b. rewrite css selectors to the appropriate files  

"""

import os
import shutil

import parse_blocks
import read_css
import write_imports
import write_css

data = parse_blocks.gather_data('./blocks')


def build_file_structure(data):
  # TODO rewrite each block.css file with imports at top
  os.mkdir('./temp-blocks')
  for block in data:
    
    write_imports.to_index_css(block)
    declarations = read_css.get_declarations(block)

    elems_and_mods = data[block]
    if elems_and_mods:
      for elem_or_mod in elems_and_mods:
        if elem_or_mod.startswith('__'):
          build_elem_file_structure(block, elem_or_mod, data, declarations)
        else:
          build_mod_file_structure(block, elem_or_mod, data, declarations, 
                                   isBlock=True)

    # write block css to temp files
    write_css.to_file(f'./temp-blocks/{block}.css', 
                      block, declarations, isBlock=True)
    # move those temp files to blocks/{block}/
    source = './temp-blocks/'
    dest = f'./blocks/{block}/{block}.css'
    files = os.listdir(source)
    for f in files:
      shutil.move(os.path.join(source, f), dest)
  os.rmdir('temp-blocks')



def build_elem_file_structure(block, elem, data, declarations):
  elem_path = os.path.join(f'./blocks/{block}/{elem}/{block}{elem}.css')
  selector = f'{block}{elem}'
  os.makedirs(os.path.dirname(elem_path), exist_ok=True)

  write_imports.to_block_css(block, elem)
  write_css.to_file(elem_path, selector, declarations)
  
  mods = data[block][elem]
  if mods:
    for mod in mods:
      build_mod_file_structure(f'{block}/{elem}', mod, data, declarations, 
                               isBlock=False, path=elem_path) 


def build_mod_file_structure(block, mod, data, declarations, isBlock=True, path=''):
  """
  isBlock - boolean indicated whether mod modifies block or element
  """
  mod_dirpath = os.path.join(f'./blocks/{block}/{mod}')
  os.makedirs(mod_dirpath, exist_ok=True)

  if not isBlock:
    block, elem = block.split('/')
    vals = data[block][elem][mod]
    
    if not vals:
      # write to block__elem_mod.css
      selector = f'{block}{elem}{mod}'
      mod_path = os.path.join(mod_dirpath, f'{selector}.css')
      write_imports.to_block_css(block, elem, mod)
      write_css.to_file(mod_path, selector, declarations)

    else:
      # write to block__elem_mod_val.css
      for val in data[block][elem][mod]:
        selector = f'{block}{elem}{mod}{val}'
        mod_path = os.path.join(mod_dirpath, f'{selector}.css')
        write_imports.to_block_css(block, elem, mod, val)
        write_css.to_file(mod_path, selector, declarations)
        
          
  else:
    # write to block_mod.css and block_mod_val.css
    vals = data[block][mod]
    write_imports.to_block_css(block, mod)

    if not vals:
        selector = f'{block}{mod}'
        mod_path = os.path.join(mod_dirpath, f'{selector}.css')
        write_css.to_file(mod_path, selector, declarations)
      
        
    else:
      for val in data[block][mod]:
        selector = f'{block}{mod}{val}'
        mod_path = os.path.join(mod_dirpath, f'{selector}.css')
        write_css.to_file(mod_path, selector, declarations)



build_file_structure(data)