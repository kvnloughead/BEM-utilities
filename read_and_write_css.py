#!usr/bin/python

import os

def index_import_statement(block):
  """Returns a block level import string"""
  url = os.path.join(f'./blocks/{block}', f'{block}.css')
  statement = f"@import url('{url}');\n"
  return statement

def to_index_css(block_import_statements):
  """Writes block_import_statements to pages/index.css."""
  index_path = os.path.join(f'./pages/index.css')
  os.makedirs(os.path.dirname(index_path), exist_ok=True)
  with open(index_path, "w") as index_css:
    index_css.write(block_import_statements)

def block_import_statement(block, elem, mod=''):
  url = os.path.join(f'./blocks/{block}/{elem}',
                     f'{mod}',
                     f'{block}{elem}{mod}.css')
  statement = f"@import url('{url}');\n"
  with open(f'./blocks/{block}/{block}.css', 'a') as block_css:
      block_css.write(statement)
