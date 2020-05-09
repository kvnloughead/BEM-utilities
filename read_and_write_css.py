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

def write_imports_to_files(data):
  """
  Creates (or overwrites) pages/index.css, iterates through
  blocks in data, writing import statements to index.css and 
  block.css by way of helper functions.
  """
  os.makedirs(os.path.dirname('./pages/index.css'), exist_ok=True)
  with open('./pages/index.css', 'w+') as index_css:
    for block in data:
      import_statement = write_import_statement(index_css, block)
      index_css.write(import_statement)
      write_imports_to_block(block, data)
      print(import_statement)

def write_imports_to_block(block, data):
  """
  Writes all necessary import statements to block.css files.
  """
  for elem in data[block]:
    if elem.startswith('__'):
      with open(f'./blocks/{block}/{elem}/{block}{elem}.css') as elem_css:
        import_statement = write_import_statement(elem_css, block, elem)
        print(import_statement)
        for mod in data[block][elem]:
          if data[block][elem][mod]:
            for val in data[block][elem][mod]:
              with open(f'./blocks/{block}/{elem}/{mod}/{block}{elem}{mod}{val}.css') as elem_css:
                import_statement = write_import_statement(elem_css, block, elem, mod, val)
                print(import_statement)
          else:
            with open(f'./blocks/{block}/{elem}/{mod}/{block}{elem}{mod}.css') as elem_css:
              import_statement = write_import_statement(elem_css, block, elem, mod)
              print(import_statement)
            
    else:
      mod = elem
      if data[block][mod]:
        print(data[block][mod])
        for val in data[block][mod]:
          print('val', val)
          with open(f'./blocks/{block}/{mod}/{block}{mod}{val}.css') as mod_css:
            import_statement = write_import_statement(mod_css, block, mod, val)
      else:
        with open(f'./blocks/{block}/{mod}/{block}{mod}.css') as mod_css:
          import_statement = write_import_statement(mod_css, block, mod)
          # print(import_statement)


def write_import_statement(filename, block, elem='', mod='', val=''):
  """
  Returns the necessary import statement.
  """
  path = os.path.join(f'./blocks/{block}', elem, mod, val)
  return path
  # mid_path = f'{elem}{mod}'
  # path = f'../blocks/{block}/'

  # path = f'../blocks/{block}/{block}'
  # if elem and mod:
  #   path = f'../blocks/{block}/{elem}/{mod}/{block}{elem}{mod}'
  # elif elem:
  #   path = 
  # statement = f"@import url('{path}');\n"
  # return statement
  

write_imports_to_files(data)
