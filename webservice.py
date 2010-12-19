#!/usr/bin/python

from musicbrainz2.webservice import *

TRACK_URI = 'http://musicbrainz.org/track/%s'

def submit_rating(conn, track, rating):
	q = Query(conn)
	q.submitUserRating( TRACK_URI % track, int(rating) )

def get_rating(conn, track):
	q = Query(conn)
	r = q.getUserRating( TRACK_URI % track )
	if r:
		return int(r.getValue())
	else:
		return 0

