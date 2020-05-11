import read_css

# block = 'a-block'

def to_file(path, selector, declarations):
  """
  Writes declarations from data gathered by read_css.py
  """
  with open(path, 'a') as f:
    for s in declarations[selector]:
      f.write(s)
    



