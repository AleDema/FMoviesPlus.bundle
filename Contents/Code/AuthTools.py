#!/usr/bin/env python
#
# AuthTools
# https://github.com/Twoure/KissNetwork.bundle
#
# Author: Twoure 
# https://github.com/Twoure
#

import urllib2

def CheckAdmin():
	"""
	For Plex Home   : Only the main users token is accepted at http://127.0.0.1:32400/myplex/account
	For All Else	: Only the main users token is accepted at https://plex.tv/users/account
	"""

	url = 'https://plex.tv/users/account' if Prefs['plextv'] else 'http://127.0.0.1:32400/myplex/account'

	Log.Debug('*' * 80)
	Log('* Checking if user is Admin')
	Log.Debug('* Auth URL   = {}'.format(url))

	ptoken = Request.Headers.get('X-Plex-Token', '')
	if not ptoken:
		Log.Error('* NO Plex Token available for validation')
		Log('* Assuming current user is Admin')
		Log.Debug('*' * 80)
		return True
	else:
		Log.Debug('* Plex Token is available for validation')
		try:
			req = urllib2.Request(url, headers={'X-Plex-Token': ptoken})
			res = urllib2.urlopen(req, timeout=10)
			if res.read():
				Log('* Current User is Admin')
				Log.Debug('*' * 80)
				return True
		except Exception as e:
			Log('* Current User is NOT Admin')
			Log.Error('* CheckAdmin: User denied access: {}'.format(e))
			Log.Debug('*' * 80)
	return False