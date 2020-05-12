import read_css

def to_file(path, selector, declarations, isBlock=False):
  """
  Writes declarations from data gathered by read_css.py
  """
  
  with open(path, 'a') as f:
    if isBlock:
      f.write('\n')
    for s in declarations[selector]:
      f.write(s)
    



