#!usr/bin/python
"""
These functions handle all of the writing to files, both of import
statements and declarations.
"""

import os

def imports_to_index(block):
  """
  Creates a block level import string amd writes it
  to pages/index.css
  """
  index_path = os.path.join(f'./pages/index.css')
  os.makedirs(os.path.dirname(index_path), exist_ok=True)
  url = os.path.join(f'./blocks/{block}', f'{block}.css')
  statement = f"@import url('{url}');\n"
  with open(index_path, "a") as index_css:
    index_css.write(statement)
    

def imports_to_block_css(block, elem, mod='', val=''):
  """
  Creates block__elem[_mod][_val] import string and
  writes string to a temporary ./{block}.css file.
  """
  url = os.path.join(f'./{elem}', f'{mod}',
                     f'{block}{elem}{mod}{val}.css')
  statement = f"@import url('{url}');\n"
  with open(f'./temp-blocks/{block}.css', 'a') as block_css:
      block_css.write(statement)

def css_to_file(path, selector, declarations, isBlock=False):
  """
  Takes declarations gathered by read_css.py and writes
  them to the appropriate css files. 
  """
  
  with open(path, 'a') as f:
    if isBlock:
      f.write('\n')
    for s in declarations[selector]:
      f.write(s)

