#!usr/bin/python
"""
Contains gather_data function which is called by build.py.  Collects
and returns block[__emel][_mod][_val] names in a nested dictionary.
"""

import os
import sys

def gather_data(block_dir='./blocks'):
  """
  Iterates through block.css files, calling parse_css_file to gather
  data on elements, modifiers and values.

  Returns a dict with this data for all blocks.
  """
  blocks = os.listdir(block_dir)
  block_data = {}
  for block in blocks:
    block_path = os.path.join(f'./blocks/{block}', f'{block}.css')
    with open(block_path, 'r') as f:
      block_data[block] = parse_css_file(f, block)
  return block_data


def parse_css_file(f, block):
  """
  Reads file (f= {block}.css) looking for selector declarations.  
  Calls the relevant handle_selector-type functions to parse 
  the different selector types.

  Selector-types:  block__elem[_mod[_val]] and block_mod[_val].  
  """
  data = {}
  for line in f:
    line = line.strip()
    if line.startswith(f'.{block}_') :
      selector = line.split(' ')[0][1:].split(':')[0]
      if '__' in selector:
        handle_element(f, block, selector, data)
      else:
        handle_modifier(f, block, selector, data)
  return data
        

def handle_element(f, block, selector, data):
  """
  Parses selectors of the form block__elem[_mod_val].
  """
  elem_mod_val = selector.split('__')[1]
  elem = elem_mod_val.split('_')[0]
  elem = f'__{elem}'

  if elem not in data:
    data[elem] = {}

  if len(elem_mod_val.split('_')) >= 2:
    handle_elem_mod_val(block, elem, elem_mod_val, data)
  
  return data

def handle_elem_mod_val(block, elem, elem_mod_val, data):
  if len(elem_mod_val.split('_')) == 2:
    mod = elem_mod_val.split('_')[1]
    mod = f'_{mod}'
    if mod not in data[elem]:
      data[elem][mod] = []
    
  if len(elem_mod_val.split('_')) == 3:
    mod, val = elem_mod_val.split('_')[1:]
    mod, val = f'_{mod}', f'_{val}'
    
    if mod not in data[elem]:
      data[elem][mod] = []
    if val not in data[elem][mod]:
      data[elem][mod].append(val)

def handle_modifier(f, block, selector, data):
  """Parses selectors of the form block_mod[_val]."""
  mod = selector.split('_')[1]
  mod = f'_{mod}'
  if mod not in data:
    data[mod] = []
  if len(selector.split('_')) == 3:
    val = selector.split('_')[2]
    val = f'_{val}'
    if val not in data[mod]:
      data[mod].append(val)
  return data
