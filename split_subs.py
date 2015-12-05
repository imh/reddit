import json
import os, os.path
import re
import itertools

def get_comment_files_in_folder(folder):
  files = []
  for (dirpath, dirnames, filenames) in os.walk(folder):
      for f in filenames:
        if len(f) == 10 and re.match('RC_20\d\d-\d\d', f) is not None:
          files.append(os.path.join(dirpath, f))
  return files

def save_lines(lines, chunk=None):
	if chunk is not None:
		print 'SORTING CHUNK %d ...' % chunk,
	lines = sorted(lines, key=lambda line: json.loads(line)['subreddit'])
	if chunk is not None:
		print 'DONE\nSAVING CHUNK %d ...' % chunk,
	for sub, group in itertools.groupby(lines, key=lambda line: json.loads(line)['subreddit']):
		with open(sub, 'a') as sub_file:
			sub_file.write(''.join(group))
	print 'DONE'

if __name__ == '__main__':
	for month_fname in get_comment_files_in_folder('../reddit_data_comments/'):
		with open(month_fname, 'r') as month_file:
			print 'BEGINNING FILE: %s' % month_fname
			i = 1
			print 'READING CHUNK %d ...' % i, 
			lines = month_file.readlines(int((1 << 31) - 1))
			print ('DONE' if lines else 'END')
			while lines:
				save_lines(lines, i)
				i += 1
				print 'READING CHUNK %d ...' % i, 
				lines = month_file.readlines(int((1 << 31) - 1))
				print ('DONE' if lines else 'END')