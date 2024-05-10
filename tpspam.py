import numpy as np
import os
import math
import re

def lireMail(fichier, dictionnaire):
	""" 
	Lire un fichier et retourner un vecteur de booléens en fonctions du dictionnaire
	"""
	
	with open(fichier, "r", encoding="ascii", errors="surrogateescape") as f:
		contenu = f.read().lower()
		mots = re.split(r'\W+', contenu)  

	return [mot in mots for mot in dictionnaire]

def charge_dico(fichier):

	with open(fichier, "r") as f:
		mots = [ligne.strip().lower() for ligne in f if len(ligne.strip()) >= 3]
	print("Chargé " + str(len(mots)) + " mots dans le dictionnaire")	

	return mots

############ apprentissage du modèle ############
def apprendBinomial(dossier,  dictionnaire):
	"""
	Fonction d'apprentissage d'une loi binomiale a partir des fichiers d'un dossier
	Retourne un vecteur b de paramètres 
		
	"""
	epsilon = 1
	compteur_mots = [epsilon] * len(dictionnaire)
	total_fichiers = 0

	for fichier in os.listdir(dossier):
		total_fichiers += 1
		chemin_fichier = os.path.join(dossier, fichier)
		vecteur = lireMail(chemin_fichier, dictionnaire)
		for i, presence in enumerate(vecteur):
			if presence:
				compteur_mots[i] += 1

	total_possibilites = total_fichiers + 2 * epsilon
	b = [count / total_possibilites for count in compteur_mots]
	return b


def prediction(x, Pspam, Pham, bspam, bham):
	"""
		Prédit si un mail représenté par un vecteur booléen x est un spam
		à partir du modèle de paramètres Pspam, Pham, bspam, bham.
		Retourne True ou False.
		
	"""
	# pour éviter les traité comme un zero 
	proba_spam = np.log(Pspam)
	proba_ham = np.log(Pham)

	for i, val in enumerate(x):
		if val:
			proba_spam += np.log(bspam[i])
			proba_ham += np.log(bham[i])
		else:
			proba_spam += np.log(1 - bspam[i])
			proba_ham += np.log(1 - bham[i])

	return proba_spam > proba_ham 

def test(dossier, isSpam, Pspam, Pham, bspam, bham, dictionnaire):
	"""
		Test le classifieur de paramètres Pspam, Pham, bspam, bham 
		sur tous les fichiers d'un dossier étiquetés 
		comme SPAM si isSpam et HAM sinon
		
		Retourne le taux d'erreur 
	"""
	fichiers = os.listdir(dossier)
	erreurs = 0
	total = len(fichiers)

	for fichier in fichiers:
		chemin_fichier = os.path.join(dossier, fichier)
		vecteur = lireMail(chemin_fichier, dictionnaire)
		predit_spam = prediction(vecteur, Pspam, Pham, bspam, bham)
		if predit_spam != isSpam:
			erreurs += 1
			print(f"*** Erreur *** {'SPAM' if isSpam else 'HAM'} {chemin_fichier} identifié incorrectement")

	taux_erreur = erreurs / total
	return taux_erreur


############ programme principal ############


# Programme principal
dossier_app = './spam/baseapp'
dossier_test = './spam/basetest'
fichier_dico = './spam/dictionnaire1000en.txt'

# Charger le dictionnaire
dictionnaire = charge_dico(fichier_dico)

# Apprentissage pour Spam
bspam = apprendBinomial(os.path.join(dossier_app, 'spam'), dictionnaire)
bham = apprendBinomial(os.path.join(dossier_app, 'ham'), dictionnaire)

# Probabilités a priori
fichiers_spam = os.listdir(os.path.join(dossier_app, 'spam'))
fichiers_ham = os.listdir(os.path.join(dossier_app, 'ham'))
Pspam = len(fichiers_spam) / (len(fichiers_spam) + len(fichiers_ham))
Pham = 1 - Pspam

# Tests
taux_erreur_spam = test(os.path.join(dossier_test, 'spam'), True, Pspam, Pham, bspam, bham, dictionnaire)
taux_erreur_ham = test(os.path.join(dossier_test, 'ham'), False, Pspam, Pham, bspam, bham, dictionnaire)
print(f"Taux d'erreur sur les spams: {taux_erreur_spam * 100:.2f}%")
print(f"Taux d'erreur sur les hams: {taux_erreur_ham * 100:.2f}%")


# Calcul du taux d'erreur total
total_spams_test = len(os.listdir(os.path.join(dossier_test, 'spam')))
total_hams_test = len(os.listdir(os.path.join(dossier_test, 'ham')))
total_mails_test = total_spams_test + total_hams_test
erreurs_totales = (taux_erreur_spam * total_spams_test) + (taux_erreur_ham * total_hams_test)
taux_erreur_total = erreurs_totales / total_mails_test
print(f"Taux d'erreur total: {taux_erreur_total * 100:.2f}%")
