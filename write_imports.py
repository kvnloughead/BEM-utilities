#!usr/bin/python

import os

def to_index_css(block):
  """Returns a block level import string"""
  index_path = os.path.join(f'./pages/index.css')
  os.makedirs(os.path.dirname(index_path), exist_ok=True)
  url = os.path.join(f'./blocks/{block}', f'{block}.css')
  statement = f"@import url('{url}');\n"
  with open(index_path, "w") as index_css:
    index_css.write(statement)
    

def to_block_css(block, elem, mod='', val=''):
  """
  Creates block__elem[_mod] import string and
  writes string to a temporary ./{block}.css file.
  """
  url = os.path.join(f'./blocks/{block}/{elem}',
                     f'{mod}',
                     f'{block}{elem}{mod}{val}.css')
  statement = f"@import url('{url}');\n"
  with open(f'./{block}.css', 'a') as block_css:
      block_css.write(statement)
  # url = os.path.join(f'./blocks/{block}/{elem}',
  #                    f'{mod}',
  #                    f'{block}{elem}{mod}{val}.css')
  # statement = f"@import url('{url}');\n"
  # with open(f'./blocks/{block}/{block}.css', 'a') as block_css:
  #     block_css.write(statement)
