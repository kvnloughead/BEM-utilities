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
  Reads css file looking for selector declarations.  Calls the relevant
  handle_selector-type functions to parse the different selector types.
  Selector-types:  block__elem[_mod[_val]] and block_mod[_val].
  """
  data = {}
  for line in f:
    line = line.strip()
    if line.startswith(f'.{block}_') :
      selector = line.split(' ')[0][1:]
      if '__' in selector:
        handle_element(f, block, selector, data)
      else:
        handle_modifier(f, block, selector, data)
  return data
        

def handle_element(f, block, selector, data):
  """
  Parses selectors of the form block__elem[_mod_val].
  """
  element = selector.split('__')[1]
  elem = element.split('_')[0]
  elem = f'__{elem}'

  if elem not in data:
    data[elem] = {}

  if len(element.split('_')) == 2:
    mod = element.split('_')[1]
    mod = f'_{mod}'
    if mod not in data[elem]:
      data[elem][mod] = []
    
  if len(element.split('_')) == 3:
    mod, val = element.split('_')[1:]
    mod, val = f'_{mod}', f'_{val}'
    
    if mod not in data[elem]:
      data[elem][mod] = []
    if val not in data[elem][mod]:
      data[elem][mod].append(val)
  
  return data


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

# Testing

def pretty_print_block_data(data):
  """Pretty prints block data from gather_data."""
  for block in data:
    print("===============")
    print(block)
    for elem in data[block]:
      print('   ', elem)
      for mod in data[block][elem]:
        print('      ', mod)
        try:
          for val in data[block][elem][mod]:
            print('         ', val)
        except TypeError:
          pass

# pretty_print_block_data(gather_data('./blocks'))

print(gather_data('./blocks'))
