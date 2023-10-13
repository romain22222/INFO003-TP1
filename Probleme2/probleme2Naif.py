#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys
from math import sqrt


# -----------------------   Votre algorithme   ------------------------------
#  L'argument l contient une liste d'entiers de taille n

def distance_min_naive(l):
	# A partir d'une liste de points (x, y), trouve la distance minimale parmi toutes les paires de points
	# Question b: O(n^2) (2 boucles for imbriquées)
	# On peut voir sur le graphique que la complexité est quadratique
	def dist(p1, p2):
		return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

	minDist = dist(l[0], l[1])

	for i in range(len(l)):
		for j in range(i + 1, len(l)):
			if dist(l[i], l[j]) < minDist:
				minDist = dist(l[i], l[j])

	return minDist


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

	val = distance_min_naive(tab)

	if verbose:
		print("Output: ")
		print(val)
