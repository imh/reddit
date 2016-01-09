import json
import os
from utils import get_chunks_of_file
import itertools

if __name__ == '__main__':
	with open('RS_full_corpus', 'r') as f:
		for lines in get_chunks_of_file(f):
			for sub, subg in 