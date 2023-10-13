#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys
from random import randrange

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generates a list of integers.')
	parser.add_argument('size', metavar='S', type=int, help='number of integers')
	parser.add_argument('--range', type=int, metavar='R', dest='range', default=-1,
						help='range of the integers (default R=S^2)')
	parser.add_argument('--tempFile', type=str, metavar='F', dest='tfile', default="",
						help='name of the temporary file (default F="integersList_S")')
	parser.add_argument('--numberByLine', type=int, metavar='N', dest='nbl', default=1, help='number of integers by line')
	args = parser.parse_args()
	S = args.size
	if args.tfile == "":
		F = "integersList_" + str(S)
	else:
		F = args.tfile
	if args.range >= 0:
		R = args.range
	else:
		R = S * S

	f = open(F, "w+")
	try:
		f.write('Liste de ' + str(S) + ' entiers :\n')
		for i in range(S):
			for j in range(args.nbl-1):
				f.write(str(randrange(R)) + ' ')
			f.write(str(randrange(R)) + '\n')
	finally:
		f.close()
