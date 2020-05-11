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
  # TODO handle pseudoelements (::) and pseudoclasses (:)
  path = f'./blocks/{block}/{block}.css'
  data = collections.defaultdict(list)
  with open(path, 'r') as block_css:
    
    lines = block_css.readlines()
    line_idx, start_idx = 0, None
    end_of_file_idx = len(lines) - 1
    while line_idx < len(lines):

      line = lines[line_idx]
      if isSelector(line, block):
        if start_idx:
          declaration = ''.join(lines[start_idx: line_idx])
          data[selector].append(declaration)
        start_idx = line_idx
        selector = line.split(' ')[0][1:]

      elif isMediaQuery(line) \
      and not isBlockSelector(lines[line_idx + 1].strip(), block):
        if start_idx:
          declaration = ''.join(lines[start_idx: line_idx])
          data[selector].append(declaration)
        start_idx = line_idx
        selector = lines[line_idx + 1].strip().split(' ')[0][1:]
      
      elif line_idx == end_of_file_idx:
        if start_idx:
          declaration = ''.join(lines[start_idx: line_idx])
          data[selector].append(declaration)

      line_idx += 1
    return data

  
     
def isSelector(line, block):
  """
  Returns if line begins a compound BEM selector for the given block.  
  Maybe one day I'll write a regex to generalize this.
  """
  return line.startswith(f'.{block}_')

def isMediaQuery(line):
  """Returns whether line starts a media query."""
  return line.startswith('@media')

def isBlockSelector(line, block):
  """Returns if line begins a BEM block selector (not element, no mods)."""
  return line.startswith(f'.{block} ')


if __name__ == '__main__':
  declarations = get_declarations('a-block')
  # print(declarations)
  for key, val in declarations.items():
    print("================================================")
    print("key", key)
    print("val", val)
    print(len(val))