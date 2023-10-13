#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys
from math import sqrt


# -----------------------   Votre algorithme   ------------------------------
def sommeMinRec(t, i):
	if i == 0:
		return 0
	option = float("inf")
	for x in [1, 3, 5]:
		if x <= i:
			tmp = t[i] + sommeMinRec(t, i - x)
			if tmp < option:
				option = tmp
	return option


def sommeMin(t, n):
	memory = t[:]
	for i in range(1, n + 1):
		datas = [memory[i - 1]]
		if i >= 3:
			datas.append(memory[i - 3])
			if i >= 5:
				datas.append(memory[i - 5])
		memory[i] += min(datas)
	return memory[n]


# -----  Fonction mère (normalement il n'y a pas à modifier la suite)  ------

#  Aide indiquant comment utiliser notre fonction
def usage(nom):
	print("Usage : " + nom + " file")
	print("  Importe un fichier file listant un ensemble d'entiers et")
	print("  applique votre algorithme sur cette liste d'entiers.")


if __name__ == '__main__':
	sys.setrecursionlimit(100000)
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
			tab.append(int(line))
	finally:
		file.close()
	if verbose:
		print("Input: ")
		print(tab)

	val = sommeMin(tab, len(tab) - 1)

	if verbose:
		print("Output: ")
		print(val)
