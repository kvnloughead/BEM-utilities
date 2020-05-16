#!usr/bin/python
"""
Reads the original block level css files and sorts declarations
into a dictionary for later writing to the new file structure.
See readme.md for details on supported css selector types.
"""

import os
import re
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
        selector, start_idx = get_declaration_block(block, line, lines, 
                                                    line_idx, start_idx, 
                                                    selector, declarations)
      elif isMediaQuery(line):
        selector, start_idx = get_declaration_block(block, line, lines, 
                                                    line_idx + 1, start_idx, 
                                                    selector, declarations)
      
      elif line_idx == end_of_file_idx:
        declaration = ''.join(lines[start_idx: line_idx + 1])
        if '_' in selector:
            declaration = fix_file_paths(selector, declaration)
            if hasModifier(selector):
              block, elem, _, _ = split_selector(selector)
              declaration = f'.{block}{elem}{declaration}'
        declarations[selector].append(declaration)

      line_idx += 1
      
    return declarations

def get_declaration_block(block, line, lines, line_idx, start_idx, selector, declarations):
      """Grabs the current declaration block and saves it to declarations.
         Handles media queries as well.

         If a file path enclosed in url(...) or src(...) is detected in any 
         declaration that will have its nesting altered (ie, non-block selectors),
         calls fix_file_paths to compensate.

         For all modified blocks and block__elements, automatically 
         increases specificity of selector selector to avoid overwriting
         the modified decarations.
      """
      line = lines[line_idx]
      new_selector = (line.strip().split(' ')[0][1:]
                                    .split(':')[0])
      if line_idx > 0:
          declaration = ''.join(lines[start_idx: line_idx])
          if hasModifier(selector):
            block, elem, _, _ = split_selector(selector)
            declaration = f'.{block}{elem}{declaration}'
          print(declaration)

          if '_' in selector:
            declaration = fix_file_paths(selector, declaration)
          declarations[selector].append(declaration)
          selector = new_selector
          start_idx = line_idx
      
      return selector, start_idx

def fix_file_paths(selector, declaration):
  """An ugly function that fixes the file paths."""
  nest_depth_increase = 1
  if len(selector.split('_')) >= 4:
    nest_depth_increase = 2
  
  paths = re.findall(r'(?:url|src)\((.*)\)', declaration)
  try:
    paths = [path.strip('\'\"') for path in paths]
    paths = [path.split('/')[0] + '/' + '../' * nest_depth_increase + '/'.join(path.split('/')[1:]) for path in paths]
    declaration = re.sub(r'((?:url|src)\()(.*)(\))', fr"\1'{paths[0]}'\3", declaration)
  except IndexError:
    pass

  return declaration

def isSelector(line, block):
  """Returns whether line begins with a BEM class selector for the 
  given block."""
  return line.startswith(f'.{block}')

def split_selector(selector):
  """Splits selector into its components, along with the necessary
  leading underscores."""
  block = elem = mod = val = ''
  if isElement(selector):
    block, elem = selector.split('__')
    if hasModifier(selector) and not hasValue(selector):
      elem, mod = elem.split('_')
    elif hasModifier(selector):
      elem, mod, val = elem.split('_')

  else:
    block = selector
    if hasModifier(selector) and not hasValue(selector):
      block, mod = selector.split('_')
    elif hasModifier(selector):
      block, mod, val = selector.split('_')
    
  if elem:
    elem = f'__{elem}'
  if mod:
    mod = f'_{mod}'
  if val:
    val = f'_{val}'

  return block, elem, mod, val

def isMediaQuery(line):
  """Returns whether line begins with a media query."""
  return line.startswith('@media')

def isElement(selector):
  """Returns whether selector is an element, not a block."""
  return len(selector.split('__')) == 2

def hasModifier(selector):
  """Returns whether selector has a modifier (with or without value)."""
  if isElement(selector):
    return '_' in selector.split('__')[1]
  return '_' in selector

def hasValue(selector):
  """Returns whether selector has a value (must have modifier also)."""
  if isElement(selector):
    return len(selector.split('__')[1].split('_')) == 3
  else:
    return len(selector.split('_')) == 3

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


  def test_fix_file_paths():
    print(fix_file_paths('block__elem', 'url("../../foo/foo.css")'))       
    print(fix_file_paths('block__elem_mod', 'src(../../foo/foo.css)'))
    print(fix_file_paths("block__elem_mod_val", "url('../../foo/foo.css')"))
    print(fix_file_paths('block_mod_val', 'src("../../foo/foo.css")'))
    print(fix_file_paths('block_mod', 'url(../../foo/foo.css)'))
    print(fix_file_paths('block__elem_mod', 'url(./../../foo/foo.css)'))
    print(fix_file_paths('block_mod', 'url(./../../foo/foo.css)'))

  def test_isElement():
    test_cases = ['block', 'block_mod', 'block_mod_val',
                  'block__elem', 'block__elem_mod', 'block__elem_mod_val'
                  ]
    expected = [
      False, False, False, True, True, True
    ]
    for i, test in enumerate(test_cases):
      print("Expected =", expected[i])
      print("Computed =", isElement(test))
      print("=========================")

  def test_hasModifier():
    test_cases = ['block', 'block_mod', 'block_mod_val',
                  'block__elem', 'block__elem_mod', 'block__elem_mod_val'
                  ]
    expected = [
      False, True, True, False, True, True
    ]
    for i, test in enumerate(test_cases):
      print("Expected =", expected[i])
      print("Computed =", hasModifier(test))
      print("=========================")

  def test_hasValues():
    test_cases = ['block', 'block_mod', 'block_mod_val',
                  'block__elem', 'block__elem_mod', 'block__elem_mod_val'
                  ]
    expected = [
      False, False, True, False, False, True
    ]
    for i, test in enumerate(test_cases):
      print("Expected =", expected[i])
      print("Computed =", hasValue(test))
      print("=========================")


  def test_split_selector():
    test_cases = ['block', 'block_mod', 'block_mod_val',
                  'block__elem', 'block__elem_mod', 'block__elem_mod_val'
                  ]
    for test in test_cases:
      print(split_selector(test))


  # test_get_declaration_blocks('a-block')
  # test_fix_file_paths()
  # test_isElement()
  # test_hasModifier()
  # test_hasValues()
  test_split_selector()


  