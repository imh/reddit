import json
from utils import get_chunks_of_file
import itertools

if __name__ == '__main__':
	with open('../RS_full_corpus', 'r') as f:
		chunk = 1
		print 'READING CHUNK %d ...' % chunk,
		for lines in get_chunks_of_file(f):
			print 'DONE\nSORTING CHUNK %d ...' % chunk,
			lines = sorted(lines, key=lambda l: json.loads(l).get('subreddit', 'NO_SUBREDDIT'))
			print 'DONE\nSAVING CHUNK %d ...' % chunk,
			for sub, g in itertools.groupby(lines, key=lambda l: json.loads(l).get('subreddit', 'NO_SUBREDDIT')):
				with open(sub, 'a') as subfile:
					subfile.write(''.join(g))
			chunk += 1
			print 'DONE\nREADING CHUNK %d ...' % chunk,
		print 'END'