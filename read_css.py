import os
import collections

block = 'footer'
file = f'./blocks/{block}/{block}.css'

def get_declarations(block):
  """
  Reads block.css gathering indices and selectors for all non-block
  level declarations.

    - Captures @media queries and . prefaced selectors.
    - Does not handle any other type of selector.

  """
  # TODO refactor into separate functions
  path = f'./blocks/{block}/{block}.css'
  data = collections.defaultdict(list)
  with open(path, 'r') as block_css:
    
    lines = block_css.readlines()
    line_idx, start_idx = 0, 0
    end_of_file_idx = len(lines) - 1

    selector = block
    while line_idx < len(lines):
      line = lines[line_idx]
      if isSelector(line, block):

        new_selector = lines[line_idx].strip().split(' ')[0][1:].split(':')[0]
        if line_idx > 0:
          declaration = ''.join(lines[start_idx: line_idx])
          data[selector].append(declaration)
          selector = new_selector
          start_idx = line_idx

      elif isMediaQuery(line):
        new_selector = lines[line_idx + 1].strip().split(' ')[0][1:].split(':')[0]
        declaration = ''.join(lines[start_idx: line_idx])
        data[selector].append(declaration)
        selector = new_selector
        start_idx = line_idx
      
      elif line_idx == end_of_file_idx:
        declaration = ''.join(lines[start_idx: line_idx])
        data[selector].append(declaration)

      line_idx += 1
      
    return data

  
     
def isSelector(line, block):
  """
  Returns if line begins a compound BEM selector for the given block.  
  Maybe one day I'll write a regex to generalize this.
  """
  return line.startswith(f'.{block}')

def isMediaQuery(line):
  """Returns whether line starts a media query."""
  return line.startswith('@media')

def isBlockSelector(line, block):
  """Returns if line begins a BEM block selector (not element, no mods)."""
  return line.startswith(f'.{block} ')


if __name__ == '__main__':

  def test_get_declarations(block):
    """
    Test for get_declarations.   Prints out all keys and 
    values (ie, selectors and declarations) obtained by that
    function for easy comparison with the original block.css.
    """
    declarations = get_declarations(block)
    for key in declarations:
      print(key)
      print("------")
      for val in declarations[key]:
        print(f'=>  {val}')
      print("=========================")

  test_get_declarations('a-block')
  