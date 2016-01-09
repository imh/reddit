import json
import itertools
import os
from utils import get_chunks_of_file, remake_folder
import pandas as pd

def get_sub_files(folder):
	filenames = os.listdir(folder)
	folder_prefix = folder + ('' if folder[-1] == '/' else '/')
	return [folder_prefix + filename for filename in filenames]


def save_lines(lines, sub_prefix, chunk):
	print 'SORTING CHUNK %d ...' % chunk,
	lines = sorted(lines, key=lambda line: json.loads(line)['link_id'])
	print 'DONE\nSAVING CHUNK %d ...' % chunk,
	for link_first4, group in itertools.groupby(lines, lambda line: json.loads(line)['link_id'][:4]):
		with open(sub_prefix + link_first4, 'a') as link_file:
			link_file.write(''.join(group))
	print 'DONE'


class StatusDF(object):
	def __init__(self, filenames):
		self.fname = 'status.csv'
		self.df = pd.DataFrame(index=filenames, columns=['done'])
		self.df.done = False
		if os.path.exists(self.fname):
			saved_df = pd.read_csv(self.fname)
			saved_df.columns = ['fnames', 'done']
			self.df.ix[saved_df[saved_df.done == True].fnames, 'done'] = True
	def completed(self, filename):
		try:
			self.df.ix[filename, 'done'] = True
			self.df.to_csv(self.fname)
		finally:
			self.df.ix[filename, 'done'] = True
			self.df.to_csv(self.fname)
	

if __name__== '__main__':
	sub_filenames = sorted(get_sub_files('../sub_files'))
	df = StatusDF(sub_filenames)
	for sub_filename in sub_filenames:
		if df.df.ix[sub_filename, 'done']:
			print '%s ALREADY COMPLETED' % sub_filename
		else:
			print '%s' % sub_filename
			sub_name = sub_filename.split('/')[-1]
			remake_folder(sub_name)
			with open(sub_filename, 'r') as sub_file:
				for i, lines in enumerate(get_chunks_of_file(sub_file, True)):
					save_lines(lines, sub_name + '/', i+1)
			df.completed(sub_filename)
