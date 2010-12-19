#!/usr/bin/python
# encoding=utf8

import rhythmdb, rb, gobject, gtk
import os, os.path

from config import *

print "mbratings loaded"

class Cache():
	def __init__(self, name):
		self.filename = os.path.join(rb.user_data_dir(), 'mbratings.' + name);
		self.f = open(self.filename, 'w')
	
	def add(self, trackid, rating):
		print >>self.f, '%s\t%d' % (trackid, rating)


#artist = db.entry_get(entry, rhythmdb.PROP_ARTIST)
#album = db.entry_get(entry, rhythmdb.PROP_ALBUM)
#title = db.entry_get(entry, rhythmdb.PROP_TITLE)
#track = db.entry_get(entry, rhythmdb.PROP_TRACK_NUMBER)
#albumid = db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_ALBUMID)
#artistid = db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_ARTISTID)
#trackid = self.db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_TRACKID)
#albumartistid =  db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_ALBUMARTISTID)


class MusicBrainzRatings(rb.Plugin):
	def __init__(self):
		rb.Plugin.__init__(self)
		self.local = Cache('local')
		self.config_dialog = None
		self.conf = Configuration()


	def entry_added(self, db, entry):
		rating = int(self.db.entry_get(entry, rhythmdb.PROP_RATING))
		if rating == 0: return
		self.total_rated += 1
		trackid = db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_TRACKID)
		if len(trackid) > 2:
			self.total_id += 1
			self.local.add(trackid, rating)


	def entry_changed(self, db, entry, changes):
		print "entry-changed: " + db.entry_get(entry, rhythmdb.PROP_TITLE) + "~" + db.entry_get(entry, rhythmdb.PROP_MUSICBRAINZ_TRACKID)
		for c in changes:
			print c.prop.value_name + ": " + repr(c.old) + "->" + repr(c.new)
			if c.prop == rhythmdb.PROP_RATING:
				print "!! rating changed!"


	def activate(self, shell):
		self.shell = shell
		self.total_rated = 0
		self.total_id = 0
		self.db = shell.get_property("db")
		self.db.connect('entry-added', self.entry_added)
		self.db.connect('entry-changed', self.entry_changed)


	def create_configure_dialog(self, dialog=None):
		if not self.config_dialog:
			self.config_dialog = MusicBrainzRatingsConfigDialog(self)
			self.config_dialog.connect('response', self.config_dialog_hide)

		self.config_dialog.present()
		return self.config_dialog

	def config_dialog_hide(self, dialog, response):
		dialog.hide()


	def deactivate(self, shell):
		print "mbratings deactivated"

