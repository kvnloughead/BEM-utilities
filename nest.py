#!/usr/bin/env python3.6
"""
This is the driver file for this program, which

  1. recieves the block/elem/mod/val data structure computed in 
     parse_blocks.py
  2. uses that data to create nested BEM file structure
  3. calls functions from write.py to write 
      a. import statements to index and block.css files
      b. rewrite css selectors to the appropriate files  

"""

import os
import shutil

import parse_blocks
import read_css
import write

data = parse_blocks.gather_data('./blocks')


def do_all_the_things(data):
  """
  Main driver function.  Takes as input the data obtained by 
  parse_blocks.py. Calls other functions in this file and 
  elsewhere to handle three major tasks:

    1. build the required nested BEM file structure.
    2. write the needed import statements to pages/index.css and 
       blocks/block.css for each block in data.
    3. rewrites css declarations from the original block.css files 
       to the appropriate places in the new nested file structure.

  """
  
  os.mkdir('./temp-blocks')
  for block in data:
    write.imports_to_index(block)
    declarations = read_css.get_declaration_blocks(block)

    elems_and_mods = data[block]
    if elems_and_mods:
      for elem_or_mod in elems_and_mods:
        if elem_or_mod.startswith('__'):
          build_elem_file_structure(block, elem_or_mod, data, 
                                    declarations)
        else:
          build_mod_file_structure(block, elem_or_mod, data, 
                                   declarations, isBlock=True)

    rewrite_block_css_files(block, data, declarations)  
  os.rmdir('./temp-blocks')

def rewrite_block_css_files(block, data, declarations):
  """Writes block level css declarations to the temporary 
  block.css files and moves them into ./blocks/{block}/{block}.css.
  """
  write.css_to_file(f'./temp-blocks/{block}.css', block, declarations, isBlock=True)
  source = './temp-blocks/'
  dest = f'./blocks/{block}/{block}.css'
  shutil.move(os.path.join(source, f'{block}.css'), dest)


def build_elem_file_structure(block, elem, data, declarations):
  """
  Makes element level subdirectories and files, writes css to
  block__elem.css files and writes element level import
  statements to the corresponding block.css.
  """
  # set things up
  elem = elem.split(':')[0]
  elem_path = f'./blocks/{block}/{elem}/{block}{elem}.css'
  os.makedirs(os.path.dirname(elem_path), exist_ok=True)
  selector = f'{block}{elem}'

  # write to files
  write.css_to_file(elem_path, selector, declarations)
  write.imports_to_block_css(block, elem)
 
  # deal with modifiers
  mods = data[block][elem]
  if mods:
    for mod in mods:
      build_mod_file_structure(f'{block}/{elem}', mod, data, 
                               declarations, isBlock=False, 
                               path=elem_path) 


def build_mod_file_structure(block, mod, data, declarations, 
                             isBlock=True, path=''):
  """
  Makes block__elem_mod and block_mod level subdirectories and files,
  writing css and import statements to the appropriate places.

  isBlock=True if the selector is of the form block_mod
  """
  mod_dirpath = os.path.join(f'./blocks/{block}/{mod}')
  os.makedirs(mod_dirpath, exist_ok=True)

  if not isBlock:
    block, elem = block.split('/')
    vals = data[block][elem][mod]
    
    if not vals:
      # write to block__elem_mod.css
      mod = mod.split(':')[0]
      selector = f'{block}{elem}{mod}'
      mod_path = os.path.join(mod_dirpath, f'{selector}.css')
      write.imports_to_block_css(block, elem, mod)
      write.css_to_file(mod_path, selector, declarations)

    else:
      # write to block__elem_mod_val.css
      for val in data[block][elem][mod]:
        val = val.split(':')[0]
        selector = f'{block}{elem}{mod}{val}'
        mod_path = os.path.join(mod_dirpath, f'{selector}.css')
        write.imports_to_block_css(block, elem, mod, val)
        write.css_to_file(mod_path, selector, declarations)
        
          
  else:
    # write to block_mod.css and block_mod_val.css
    vals = data[block][mod]
    write.imports_to_block_css(block, mod)

    if not vals:
        mod = mod.split(':')[0]
        selector = f'{block}{mod}'
        mod_path = os.path.join(mod_dirpath, f'{selector}.css')
        write.css_to_file(mod_path, selector, declarations)
      
        
    else:
      for val in data[block][mod]:
        val = val.split(':')[0]
        selector = f'{block}{mod}{val}'
        mod_path = os.path.join(mod_dirpath, f'{selector}.css')
        write.css_to_file(mod_path, selector, declarations)

do_all_the_things(data)