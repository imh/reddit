import json

def get_chunks_of_file(f, print_chunks=False):
  lines = f.readlines(int((1 <<31) - 1))
  while lines:
    next_lines = f.readlines(int((1 <<31) - 1))
    yield(lines, bool(next_lines))
    lines = next_lines

def extract_relevant_fields(dct):
  dct2 = {key:dct[key] for key in ['author', 'body', 'score', 'created_utc']}
  dct2['children'] = []
  return dct2

def get_children_of(name, nodes, children_of):
  """ Creates a dictionary from nodes with tree structure in the 'children'
  fields based on the tree structure in 'children_of' with root at 'name'.
  Will not terminate if 'children_of' contains cycles.
  Will not be correct if 'children_of' is not tree structured.
  """
  children = []
  for child_name in children_of[name]:
    node = nodes[child_name]
    node['children'] = get_children_of(child_name, nodes, children_of)
    children.append(node)
  return children

def create_graph(lines):
  nodes = {}
  children_of = {}
  link = None
  for line in lines:
    dct = json.loads(line)
    name = dct['name']
    parent = dct['parent']
    nodes[name] = extract_relevant_fields(dct)
    if parent.startswith('t3_'):
      link = parent
    children = children_of.get(parent, [])
    children.append(name)
    children_of[parent] = children
  top_level = {'link':link}
  top_level['children'] = get_children_of(link, nodes, children_of)
  return top_level

def tokenize_string(s, compiled=True):
  """Tokenized a string into a list of ASCII strings."""
  #TODO this is slow, but  would be simple and fast in C.
  s = s.lower()
  # if unicode_subs:
  #   #TODO replace whatever needs replacing
  #   s = s.replace(unichr(8220), '"') # Left double quote
  #   s = s.replace(unichr(8221), '"') # Right double quote
  #   s = s.replace(unichr(8212), '-') # em-dash
  #   s = s.replace(unichr(8230), '...') # Horizontal ellipses
  #   s = s.replace(unichr(8211), '-') # en-dash
  # Add spaces around punctuation so that it gets its own token
  for c in '~`!@#$%^&*()_-+={[]}|\\:;\'"<.>/?':
    s = s.replace(c,' '+c+' ')
  # Replace a few different unicode symbols
  # Replace newline so that tokenization can be saved split by newlines
  s = s.replace('\r\n', ' <NEWLINE> ')
  s = s.replace('\r', ' <NEWLINE> ')
  s = s.replace('\n', ' <NEWLINE> ')
  # Replace tab so it's recognizable
  s = s.replace('\t', ' <TAB> ')
  # Replace comma, so that tokenization can be saved comma delimited
  s = s.replace(',', ' <COMMA> ')
  # Replace non-(printable) ascii characters because they screw things up
  s = ''.join([str(char) if ord(char) < 127 and ord(char) > 31 \
                       else ' <U+%s> ' % clean_hex(ord(char)) for char in s])
  # Split words, removing redundant whitespace
  return [w for w in s.split(' ') if w.replace(' ', '') != '']

def clean_hex(x):
  return hex(x)[2:] if x >= 0 else '-' + hex(x)[3:]
