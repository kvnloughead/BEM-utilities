#!usr/bin/python
"""
Program that

  1. Recieves data from parse_blocks.py and runs build.py.

  2. Writes all necessary import statements to pages/index.css and 
     all blocks/block.css files.

  3. Reads block.css files, reading declarations and writing them to 
     the correct nested file.

"""

import os
import parse_blocks, build

data = parse_blocks.gather_data('./blocks')
build.build_file_structure(data)

def write_index_css_file():
  """
  Creates (or overwrites) pages/index.css, iterates through
  blocks in data and calls write_import_statments for each.
  """
  os.makedirs(os.path.dirname('./pages/index.css'), exist_ok=True)
  with open('./pages/index.css', 'w+') as index_css:
    for block in data:
      import_statement = write_import_statement(block, index_css)
      index_css.write(import_statement)

def write_import_statement(block, filename):
  """
  Returns the necessary import statement.
  """
  url = f'../blocks/{block}/{block}.css'
  statement = f'@import url("{url}");\n'
  return statement
  






write_index_css_file()
