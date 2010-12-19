#!/usr/bin/python
# encoding=utf8

from musicbrainz2.webservice import *

TRACK_URI = 'http://musicbrainz.org/track/%s'

def submit_rating(conn, track, rating):
	''' Submits a rating for a track UUID'''
	q = Query(conn)
	q.submitUserRating( TRACK_URI % track, int(rating) )


def get_rating(conn, track):
	''' Gets a rating for a track UUID '''
	q = Query(conn)
	r = q.getUserRating( TRACK_URI % track )
	if r:
		return int(r.getValue())
	else:
		return 0

