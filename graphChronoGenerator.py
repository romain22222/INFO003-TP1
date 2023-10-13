#!/usr/local/bin/python3
import subprocess
# -*- coding: utf-8 -*-
from json import load
from time import time
from math import log, sqrt, floor
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np
import sys
from os import listdir

CONST_MIN_RUNTIME = 0.25
CONST_EPSILON = 1e-18


def getRunTime(execfile, genefile, tempfile, input, numberByLine):
	"""
	Retourne le temps d'execution du programme ``execfile`` avec, en entree, le
	nombre ``input``.
	"""
	nbIter = 0
	tps_generator = 0.0
	avant = time()
	while time() - avant < CONST_MIN_RUNTIME:
		debut_generator = time()
		subprocess.check_output("{} {} --tempFile {} --numberByLine {}".format(genefile, input, tempfile, numberByLine),
								shell=True)
		tps_generator += time() - debut_generator
		subprocess.check_output("{} {}".format(execfile, tempfile), shell=True)
		nbIter += 1
	temps = (time() - avant - tps_generator) / nbIter
	return temps


def makeRuntimes(data):
	"""
	Calcule les temps d'executions.
	"""
	timings = []
	x = data['valeurInitiale']
	temps = 0
	wastedTimePerIteration = getRunTime(data['executable'], data['generator'], data['temp_file'], x,
										data["numberByLine"])
	while x < data['borneSup'] and temps < data['attenteMax']:
		temps = getRunTime(data['executable'], data['generator'], data['temp_file'], int(x),
						   data["numberByLine"]) - wastedTimePerIteration
		if temps < 1e-3:
			print("# Input {} is too small, insignificant timing.".format(x))
		else:
			print('# Input {}, {} millisecondes'.format(x, 1000 * temps))
			timings.append((x, 1000 * temps))
		x = eval(data['increment'])
	data['timings'] = timings


replacements = {
	'sin': 'np.sin',
	'cos': 'np.cos',
	'log': 'np.log',
	'exp': 'np.exp',
	'^': '**',
}


def stringToFunc(string):
	""" Évalue la chaîne et retourne une fonction de x """
	for old, new in replacements.items():
		string = string.replace(old, new)

	def func(x):
		return eval(string)

	return func


def optimizeCoeff(pts, func, logScale):
	"""
	Calcule le coefficient multiplicatif qui permet d'aligner la fonction
	``func`` aux données ``pts``. Il est important de noter que le coefficient
	calculé n'essaye de "fitter" qu'une seule valeur. Le choix de la valeur dépend
	de l'utilisation, ou non, d'une échelle logarithmique lors de l'affichage
	des courbes."
	"""
	f = stringToFunc(func)
	minX = min(map(lambda xy: xy[0], pts))
	maxX = max(map(lambda xy: xy[0], pts))
	if logScale:
		objectif = (sqrt(maxX * minX))
	else:
		objectif = minX + ((maxX - minX) / 2)

	# Définition de la fonction erreur
	midValues = pts[0]
	for x, y in pts:
		if abs(x - objectif) < abs(midValues[0] - objectif):
			midValues = (x, y)
	erreur = lambda coeff: abs(coeff * f(midValues[0]) - midValues[1])

	try:
		# borne inf
		a = CONST_EPSILON
		err_a = erreur(a)

		# borne sup
		b = 1.0
		err_b = erreur(2 * b)
		err_2b = erreur(2 * b)
		while err_b > err_2b:
			b *= 2
			err_b = err_2b
			err_2b = erreur(2 * b)

		# dichotomie
		l = []
		while b - a >= CONST_EPSILON:
			m = (a + b) / 2
			if m == a or m == b:  # limite de la précision des float
				return m
			if err_a < err_b:
				b = m
				err_b = erreur(b)
			else:
				a = m
				err_a = erreur(a)
		if err_a < err_b:
			return a
		else:
			return b
	except OverflowError:
		return 0


def findCoeff(data):
	"""
	Calcule les coefficients multiplicatifs à ajouter à chacune des fonctions
	décrites dans l'entrée "courbesSup".
	"""
	data['coeff'] = []
	for f in data['courbesSup']:
		data['coeff'].append(optimizeCoeff(data['timings'], f, data['logScale']))


def buildPlotCommands(data):
	plt.xlabel('Input size')
	plt.ylabel('Runtime (millisec)')
	if data['logScale']:
		plt.yscale('log')
		plt.xscale('log')
	xmin = min(map(lambda x: x[0], data['timings']))
	xmax = max(map(lambda x: x[0], data['timings']))
	ymin = 1  # min( map( lambda x : x[1], data['timings'] ) )
	ymax = max(map(lambda x: x[1], data['timings']))
	x = np.linspace(np.float64(xmin), np.float64(xmax), 100)
	plt.axis([xmin, xmax, ymin, ymax])
	np.seterr(all='ignore')
	for coeff, extraCurve in zip(data['coeff'], data['courbesSup']):
		curveName = "{:.2E}*{}".format(Decimal(coeff), extraCurve)
		plt.plot(x, stringToFunc(str(coeff) + '*' + extraCurve)(x), label=curveName)
	x, y = zip(*data['timings'])
	plt.plot(x, y, label="Execution time", linestyle="--", color='black')
	plt.legend()
	plt.savefig(data['outputImageName'], dpi=500, bbox_inches='tight')

	#  --------  Si jamais il y a un soucis avec la librairie matplotlib  ---------
	"""
	On doit toujours pouvoir récupérer les commandes pour utiliser gnuplot			 
	Construit la liste des commandes pour configurer l'outil gnuplot....
	"""


# commands = ''
# commands = 'set term pngcairo size {}\n'.format( data['outputImageSize'] )
# if data['logScale'] :
#	commands += 'set logscale xy\n'
# commands += 'set output "{}"\n'.format( data['outputImageName'] )
# commands += 'set xlabel "Input size"\n'
# commands += 'set ylabel "Runtime (millisec)"\n'
# xmin = min( map( lambda x : x[0], data['timings'] ) )
# xmax = max( map( lambda x : x[0], data['timings'] ) )
# ymin = min( map( lambda x : x[1], data['timings'] ) )
# ymax = max( map( lambda x : x[1], data['timings'] ) )
# commands += 'set xrange [{}:{}]\n'.format( xmin, xmax )
# commands += 'set yrange [{}:{}]\n'.format( ymin, ymax )
# commands += 'set key on left\n'.format( ymin, ymax )
# commands += 'set style func linespoints\n'
# commands += 'plot '
# i = 1
# for coeff,extraCurve in zip( data['coeff'], data['courbesSup'] ) :
#	curveName = "{:.2E}*{}".format( Decimal(coeff), extraCurve )
#	commands += '{}*({}) ls {} title "{}", '.format( \
#					   coeff, extraCurve, i, curveName )
#	i += 1
# commands += '"-" using 1:2 with lines lw 2 lt rgb "black" title "Execution time"\n'
# commands += '\n'.join( "{} {}".format(x,y) for x,y in data['timings'] )
# commands += '\nreplot\n'
# data['gnuplotCommands'] = commands
# print(commands)


def buildImageName(data):
	"""
	Détermine le nom à donner au fichier contenant l'image produite. Ce nom est
	déterminé en fonction de l'entrée "outputImageNamePrefix" et des fichiers
	déjà présents dans le dossier.

	Si python2.? au lieu de python3.? est installé sur votre ordinateur, commentez ces 
	lignes et modifier le nom directement dans testData.json. 
	"""
	prefix = data['outputImageNamePrefix'];
	# Si Python2.?, essayer plutôt 
	# L = listdir('.')
	L = listdir()
	mval = 1
	for name in L:
		if len(name) >= len(prefix) + 6:
			if name[:len(prefix)] == prefix and name[len(prefix)] == '-' and name[-4:] == ".png" and name[
																									 len(prefix) + 1:-4].isdigit():
				if int(name[len(prefix) + 1:-4]) >= mval:
					mval = int(name[len(prefix) + 1:-4]) + 1
	name = '{}-{}.png'.format(prefix, mval)
	data['outputImageName'] = name


if __name__ == '__main__':
	fichier = open(sys.argv[1])
	try:
		data = load(fichier)
	finally:
		fichier.close()

	makeRuntimes(data)
	findCoeff(data)
	buildImageName(data)
	buildPlotCommands(data)
	print("Done, see {} for ouput.".format(data['outputImageName']))
