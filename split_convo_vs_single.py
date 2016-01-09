from utils import create_graph, remake_folder
import os, os.path
import itertools
import json

def get_post_groups(folder):
	if folder[-1] != '/':
		folder += '/'
	subs = next(os.walk(folder))[1]
	return [(folder + sub, sub) for sub in subs]

def get_total_children_score(node):
	n = 0
	score = 0
	for child in node['children']:
		(total_children, children_score) = get_total_children_score(child)
		n += 1 + total_children
		score += child['score'] + children_score
	return (n, score)

def get_immediate_children_score(node):
	n = 0
	score = 0
	for child in node['children']:
		n += 1
		score += child['score']
	return (n, score)

def make_singles(graph):
	new_graph = {k:v for (k, v) in graph.iteritems() if k != 'children'}
	new_graph['children'] = []
	for child in graph['children']:
		(total_children, total_children_score) = get_total_children_score(child)
		(immediate_children, immediate_children_score) = get_immediate_children_score(child)
		new_child = {k:v for k in child if k != 'children'}
		new_child['total_children'] = total_children
		new_child['total_children_score'] = total_children_score
		new_child['immediate_children'] = immediate_children
		new_child['immediate_children_score'] = immediate_children_score
		new_graph['children'].append(new_child)
	return new_graph


if __name__ == '__main__':
	remake_folder('singles')
	remake_folder('convos')
	subs = get_post_groups('../comments_by_posts')
	for (subdir, sub) in subs:
		remake_folder('singles/' + sub)
		link_groups = os.listdir(subdir)
		for link_group in link_groups:
			with open(subdir + '/' + link_group, 'r') as f:
				comments = [json.loads(line) for line in f.readlines()]
				comments = sorted(comments, key=lambda comment: comment['link_id'])
				singles = []
				convos = []
				for link, g in itertools.groupby(comments, key=lambda comment: comment['link_id']):
					graph = create_graph(g)
					singles.append(make_singles(graph))
					convo_graph = make_convos(graph)
					if len(convo_graph['children']) != 0:
						convos.append(make_convo)
				with open
			break
		break
