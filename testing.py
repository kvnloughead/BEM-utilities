import parse_blocks

data = parse_blocks.gather_data('./blocks')

def pretty_print_block_data(data):
  """Pretty prints block data from gather_data."""
  for block in data:
    print("===============")
    print(block)
    for elem in data[block]:
      print('   ', elem)
      for mod in data[block][elem]:
        print('      ', mod)
        try:
          for val in data[block][elem][mod]:
            print('         ', val)
        except TypeError:
          pass

pretty_print_block_data(data)