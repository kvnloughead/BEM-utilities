#!usr/bin/python
"""
Reads the original block level css files and sorts declarations
into a dictionary for later writing to the new file structure.
See readme.md for details on supported css selector types.
"""

import os
import collections

def get_declaration_blocks(block):
  """
  Reads {block}.css sorting all declarations into a dict of the form
  declarations = {selector: ['declaration1', 'declaration2', ...]}.
  """
  path = f'./blocks/{block}/{block}.css'
  declarations = collections.defaultdict(list)
  with open(path, 'r') as block_css:
    
    lines = block_css.readlines()
    line_idx, start_idx = 0, 0
    end_of_file_idx = len(lines) - 1

    selector = block
    while line_idx < len(lines):

      line = lines[line_idx]
      if isSelector(line, block):
        selector, start_idx = get_declaration_block(line, lines, line_idx, 
                                                    start_idx, selector, 
                                                    declarations)
      elif isMediaQuery(line):
        selector, start_idx = get_declaration_block(line, lines, line_idx + 1, 
                                                    start_idx, selector, 
                                                    declarations)
      
      elif line_idx == end_of_file_idx:
        declaration = ''.join(lines[start_idx: line_idx])
        declarations[selector].append(declaration)

      line_idx += 1
      
    return declarations

def get_declaration_block(line, lines, line_idx, start_idx, selector, declarations):
      """Grabs the current declaration block and saves it to declarations.
         Handles media queries as well.
      """
      line = lines[line_idx]
      new_selector = (line.strip().split(' ')[0][1:]
                                    .split(':')[0])
      if line_idx > 0:
          declaration = ''.join(lines[start_idx: line_idx])
          declarations[selector].append(declaration)
          selector = new_selector
          start_idx = line_idx
      return selector, start_idx

def isSelector(line, block):
  """Returns whether line begins with a BEM class selector for the 
  given block."""
  return line.startswith(f'.{block}')

def isMediaQuery(line):
  """Returns whether line begins with a media query."""
  return line.startswith('@media')


if __name__ == '__main__':

  def test_get_declaration_blocks(block):
    """
    Testing function for get_declaration_blocks. Prints out all keys and 
    values (ie, selectors and declarations) obtained by that
    function for easy comparison with the original block.css.
    """
    declarations = get_declaration_blocks(block)
    for key in declarations:
      print(key)
      print("------")
      for val in declarations[key]:
        print(f'=>  {val}')
      print("=========================")

  test_get_declaration_blocks('a-block')
  