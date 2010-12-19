#!/usr/bin/python
# encoding=utf8

import gobject, gtk, gconf, rhythmdb, rb
from webservice import *

GCONF_DIR = '/apps/rhythmbox/plugins/mbratings'
GCONF_KEYS = {
	'username' : GCONF_DIR + '/username',
	'password' : GCONF_DIR + '/password'
}

class Configuration():
	def __init__(self):
		self.gconf = gconf.client_get_default()

	def get_username(self):
		return self.gconf.get_string(GCONF_KEYS['username'])

	def set_username(self, new):
		print 'set username=%s' % new
		self.gconf.set_string(GCONF_KEYS['username'], new + "!!")

def get_password(self):
		return self.gconf.get_string(GCONF_KEYS['password'])

	def set_password(self, new):
		print 'set password=%s' % new
		self.gconf.set_string(GCONF_KEYS['password'], new + "!!")

	def get_webservice(self):
		print 'usr=%s pwd=%s' % (self.get_username(), self.get_password())
		return WebService(username=self.get_username(), password=self.get_password())



class MusicBrainzRatingsConfigDialog(gtk.Dialog):
	def __init__(self, plugin):
		gtk.Dialog.__init__(self)
		self.plugin = plugin

		self.set_border_width(12)

		builder = gtk.Builder()
		builder.add_from_file(plugin.find_file('config.glade'))
		self.get_content_area().add(builder.get_object('vbox'))

		self.add_action_widget(gtk.Button(stock=gtk.STOCK_CLOSE), 0)
		self.show_all()

		builder.get_object('username').set_text(plugin.conf.username or '')
		builder.get_object('password').set_text(plugin.conf.password or '')

		self.login_test_default = 'Test Login'
		self.login_test = builder.get_object('login-test')
		self.login_test.set_label(self.login_test_default)

		builder.connect_signals(self)


	def username_changed(self, box):
		print "username changed"
		self.plugin.conf.set_username(box.get_text())
		self.login_test.set_label(self.login_test_default)


	def password_changed(self, box):
		print "password changed"
		self.plugin.conf.set_password(box.get_text())
		self.login_test.set_label(self.login_test_default)


	def test_login(self, btn):
		print "TEST LOGIN"
		try:
			print "get conn"
			conn = self.plugin.conf.get_webservice()
			track = '0e7e3366-1795-4545-891d-170a35a44b06'
			print "submit rating"
			submit_rating(conn, track, 2)
			print "ok"
		except ConnectionError, e:
			print e
			btn.set_label('Server unreachable')
		except AuthenticationError, e:
			print e
			btn.set_label('Invalid credentials')
		except Exception, e:
			print e
			btn.set_label(str(e))
		else:
			btn.set_label('Success!')

		print "DONE"


gobject.type_register(MusicBrainzRatingsConfigDialog)
