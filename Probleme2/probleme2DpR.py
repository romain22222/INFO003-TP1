#!/usr/local/bin/python3

# -*- coding: utf-8 -*-
import sys
from math import sqrt


# -----------------------   Votre algorithme   ------------------------------
#  L'argument l contient une liste d'entiers de taille n

def distance_min_diviser_pour_regner(points):
	def dist(p1, p2):
		return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

	if len(points) <= 3:
		minD = float('inf')
		for i in range(len(points)):
			for j in range(i + 1, len(points)):
				minD = min(minD, dist(points[i], points[j]))
		return minD

	points = sorted(points, key=lambda x: x[0])

	middle = len(points) // 2
	left = points[:middle]
	right = points[middle:]

	dLeft = distance_min_diviser_pour_regner(left)
	dRight = distance_min_diviser_pour_regner(right)

	minD = min(dLeft, dRight)

	toCheck = []
	for point in points:
		if abs(point[0] - points[middle][0]) < minD:
			toCheck.append(point)

	toCheck.sort(key=lambda x: x[1])
	for i in range(len(toCheck)):
		for j in range(i + 1, len(toCheck)):
			if toCheck[j][1] - toCheck[i][1] >= minD:
				break
			minD = min(minD, dist(toCheck[i], toCheck[j]))

	return minD


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

	val = distance_min_diviser_pour_regner(tab)

	if verbose:
		print("Output: ")
		print(val)
