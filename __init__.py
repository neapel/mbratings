#!/usr/bin/python
# encoding=utf8

import rhythmdb, rb, gobject, gtk, Queue
import os, os.path
from threading import Thread

from config import *
from cache import *


class MusicBrainzRatings(rb.Plugin):
	''' The main plugin class, also does the work. '''

	def __init__(self):
		''' Start worker thread etc '''
		rb.Plugin.__init__(self)
		self.queue = Queue.Queue()
		self.remote = Cache('remote')
		self.config_dialog = None
		self.conf = Configuration()
		self.untagged = 0
		self.submitter_thread = Thread(target=self.submitter)
		self.submitter_thread.start()


	def post(self, track, rating):
		''' Enqueue a rating if it is different from server. '''
		if len(track) > 2:
			if self.remote.get(track) != rating:
				self.queue.put((track, rating))
		else:
			self.untagged += 1


	def submitter(self):
		''' Waits on the queue and submits ratings to server. '''
		while True:
			track, rating = self.queue.get(True, None)
			print 'submitting %s=%d, queued %d' % (track, rating, self.queue.qsize())
			conn = self.conf.get_webservice()
			submit_rating(conn, track, rating)
			self.remote.add(track, rating)
			self.queue.task_done()


	def entry_added(self, db, entry):
		''' Called for every track added (whole library on startup!) '''
		rating = int(self.db.entry_get(entry, rhythmdb.PROP_RATING))
		if rating == 0: return
		track = db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_TRACKID)
		self.post(track, rating)


	def entry_changed(self, db, entry, changes):
		''' Called for every track changed '''
		for change in changes:
			if change.prop == rhythmdb.PROP_RATING:
				track = db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_TRACKID)
				self.post(track, int(change.new))


	def activate(self, shell):
		''' Entry point '''
		self.shell = shell
		self.db = shell.get_property('db')
		self.db.connect('entry-added', self.entry_added)
		self.db.connect('entry-changed', self.entry_changed)


	def create_configure_dialog(self, dialog=None):
		''' Open configure dialog '''
		print 'dialog=%s' % repr(dialog)
		if not self.config_dialog:
			self.config_dialog = MusicBrainzRatingsConfigDialog(self)
			self.config_dialog.connect('response', self.config_dialog_hide)

		self.config_dialog.present()
		return self.config_dialog

	def config_dialog_hide(self, dialog, response):
		''' Close configure dialog '''
		dialog.hide()


	def deactivate(self, shell):
		''' Clean up '''
		self.remote.close()

