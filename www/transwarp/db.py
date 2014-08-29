#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'GongMH'

'''
Database operation module.
'''

import time, uuid, functools, threading, logging

# Dict object:
class Dict(dict):
	"""Simple dict but support access as x.y style.

	"""
	def __init__(self, names=(), values=(), **kw):
		super(Dict, self).__init__(**kw)
		for k, v in zip(names,values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributsError(r"'Dict' object has no attributes '%s'" %key)

	def __setattr__(self, key, value):
		self[key] = value

engine = None

class _Engine(object):
	def __init__(self, connect):
		self._connect = connect
	def connect(self):
		return self._connect()

def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
	import mysql.connector
	global engine

	if engine is not None:
		raise DBError('Engine is already initialized.')
	params = dict(user=user, password=password, database=database, host=host, port=port)
	defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
	for k, v in defaults.iteritems():
		params[k] = kw.pop(k, v)
	params.update(kw)
	params['buffered'] = True
	engine = _Engine(lambda: mysql.connector.connect(**params))
	logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	create_engine('www-data', 'www-data', 'test')