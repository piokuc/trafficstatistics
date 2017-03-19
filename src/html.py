#!/usr/bin/env python

""" 
This module provides HTML rendering.
It's only used to generate some API examples at http://trafficstatistics.uk/
"""

def attr_string(attrs):
	def fix(x):
		if x.startswith('_'):
			return x[1:]
		return x
	s = ''.join(['%s="%s" ' % (fix(k), v) for k,v in attrs.items()])
	return ' ' + s[:-1]

#PK
def evalbody(*body):
	if len(body) == 0: return ''
	if type(body[0]) == type(['a list']) or type(body[0]) == type(('a tuple',)):
		return evalbody(*body[0]) + ' ' + evalbody(*body[1:])
	else:
		return str(body[0]) + ' ' + evalbody(*body[1:])
		
def entag(tagname, attrs, body):
	if attrs:
		return entag_attrs('<%s%s>' % (tagname, attr_string(attrs)),
					'</%s>' % (tagname))
	body = evalbody(body)
	return '<%(tagname)s>%(body)s</%(tagname)s>' % locals()

def entag_attrs(start, end):
	return lambda *body: start + evalbody(body) + end

class _HTML:
	def __getattr__(self, name):
		try:
			return self.__dict__[name]
		except KeyError:
			if name.endswith('_'):
				fn = lambda **attrs: '<%s%s />' % (name[:-1], attr_string(attrs))
			else:
				fn = lambda *body, **attrs: entag(name, attrs, body)
			return fn
html = _HTML()

#print html.a(href = 'http://kuchta.co.uk', target = '_top')("Peter's Homepage")
