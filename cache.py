#!/usr/bin/python
# encoding=utf8

import anydbm, os, os.path, rb, Queue

class Cache():
	''' Caches ratings sent to server in DBM file. '''

	def __init__(self, name):
		self.filename = os.path.join(rb.user_data_dir(), 'mbratings.' + name);
		self.db = anydbm.open(self.filename, 'c')

	def close(self):
		self.db.close()

	def add(self, track, rating):
		self.db[track] = str(rating)
		self.db.sync()

	def remove(self, track):
		del self.db[track]

	def get(self, track):
		if self.db.has_key(track):
			return int(self.db[track])
		return 0

	def __iter__(self):
		for k, v in self.db.iteritems():
			yield k, int(v)

	def __len__(self):
		return len(self.db)


