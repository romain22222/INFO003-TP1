#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys
from math import sqrt


# -----------------------   Votre algorithme   ------------------------------
#  L'argument l contient une liste d'entiers de taille n

def progOn2(l):
	s = 0
	for v in l:
		for w in l:
			s += v[0] * w[0]
	return s


# -----  Fonction mère (normalement il n'y a pas à modifier la suite)  ------

#  Aide indiquant comment utiliser notre fonction
def usage(nom):
	print("Usage : " + nom + " file")
	print("  Importe un fichier file listant un ensemble d'entiers et")
	print("  applique votre algorithme sur cette liste d'entiers.")


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Ce programme nécessite un fichier en argument.")
		usage(sys.argv[0])
		exit(1)

	verbose = True
	if len(sys.argv) >= 3 and sys.argv[1] == "--mute":
		verbose = False
		filename = sys.argv[2]
	else:
		filename = sys.argv[1]

	tab = []
	file = open(filename, "r")
	try:
		next(file)
		for line in file:
			tab.append([int(x) for x in line.split(" ")])
	finally:
		file.close()
	if verbose:
		print("Input: ")
		print(tab)

	val = progOn2(tab)

	if verbose:
		print("Output: ")
		print(val)
