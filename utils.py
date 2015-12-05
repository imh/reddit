
def get_chunks_of_file(f, chunk=None):
  if chunk is not None:
    print 'READING CHUNK %d ...' % chunk,
  lines = f.readlines(int((1 <<31) - 1))
  if chunk is not None:
      print ('DONE' if lines else 'END')
  while lines:
    yield lines
    if chunk is not None:
      chunk += 1
      print 'READING CHUNK %d ...' % chunk,
    lines = f.readlines(int((1 <<31) - 1))  
    if chunk is not None:
      print ('DONE' if lines else 'END')

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
