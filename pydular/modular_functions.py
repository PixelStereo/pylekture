
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

#################
# Modular Module functions for Python
# Usefull functions for dealing with models and parameters
# Pixel Stereo - 2015
################################

def m_clip(self,value):
	if self.rangeClipmode == 'low' or self.rangeClipmode == 'both':
		if value < self.rangeBounds[0]:
			value = self.rangeBounds[0]
	if self.rangeClipmode == 'high' or self.rangeClipmode == 'both':
		if value > self.rangeBounds [1]:
			value = self.rangeBounds[1]
	return value

def m_bool(args):
	if type(args) != bool:
		if debug :print ('this is expected to be a boolean, but this is a', type(args),args)
		try :
			args = args[0]
		except:
			pass
		if args == 1:
			args = True
		elif args == 0:
			args = False
		if debug :print ('now this is', type(args),args)
	return args

def m_int(args):
	args = args[0]
	if type(args) != int:
		int_args = int(args)
		if debug :print (type(args),args,'this is expected to be an integer, now it is',type(int_args),int_args)
		args = int_args
	return args

def m_string(args):
	if type(args) == int or type(args) == float:
		args = str(args)
	if type(args) != str:
		if debug :print ('this is expected to be a string, but this is a', type(args),args)
	print ('type-m_string' , type(args) , args)
	return args