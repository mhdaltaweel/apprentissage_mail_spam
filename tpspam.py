import numpy as np
import os
import math

def lireMail(fichier, dictionnaire):
	""" 
	Lire un fichier et retourner un vecteur de booléens en fonctions du dictionnaire
	"""
	# f = open(fichier, "r",encoding="ascii", errors="surrogateescape")
	# mots = f.read().split(" ")
	
	with open(fichier ,"r" ,encoding="ascii", errors="surrogateescape" ) as f:

		mots = f.read().lower().split()

	x = [False] * len(dictionnaire) 

	# à modifier... c'est fait
	mots_du_mail = set(mots)

	for index, mot in enumerate(dictionnaire):
		if mot in mots_du_mail:
			x[index] = True

	# f.close()
	return x

def charge_dico(fichier):
	f = open(fichier, "r")
	mots = f.read().split("\n")
	print("Chargé " + str(len(mots)) + " mots dans le dictionnaire")
	f.close()
	return mots[:-1]

# apprentissage du modèle 
def apprendBinomial(dossier, fichiers, dictionnaire):
	"""
	Fonction d'apprentissage d'une loi binomiale a partir des fichiers d'un dossier
	Retourne un vecteur b de paramètres 
		
	"""
	compteur_mots = [0] - len(dictionnaire)
	total_fichiers = len(fichiers)

	for fichier in fichiers:
		chemin_fichier = os.path.join(dossier, fichier)
		with open (chemin_fichier , "r" ,encoding="ascii", errors="surrogateescape") as f:
			contenu = f.read().lower().split()
		mot_du_fichier = set(contenu.split())


		for i , mot in  enumerate(dictionnaire):
			if mot in mot_du_fichier :
				compteur_mots[i] +=1
	b = [count / total_fichiers for count in compteur_mots]	# à modifier...
	return b


def prediction(x, Pspam, Pham, bspam, bham):
	"""
		Prédit si un mail représenté par un vecteur booléen x est un spam
		à partir du modèle de paramètres Pspam, Pham, bspam, bham.
		Retourne True ou False.
		
	"""
	# pour éviter les traité comme un zero 
	proba_spam = np.log(Pspam) 
	proba_ham  = np.log(Pham)

	for i in range(len(x)):
		if x[i]:
			proba_spam += np.log(bspam[i])
			proba_ham += np.log(bham[i])
		else:
			proba_spam += np.log(1- bspam[i])
			proba_ham += np.log(1- bham[i])
	return proba_spam > proba_ham  # à modifier...
	
def test(dossier, isSpam, Pspam, Pham, bspam, bham):
	"""
		Test le classifieur de paramètres Pspam, Pham, bspam, bham 
		sur tous les fichiers d'un dossier étiquetés 
		comme SPAM si isSpam et HAM sinon
		
		Retourne le taux d'erreur 
	"""
	fichiers = os.listdir(dossier)
	for fichier in fichiers:
		print("Mail " + dossier+"/"+fichier)		

		
		# à compléter...

	return 0  # à modifier...


############ programme principal ############

dossier_spams = "./spam/baseapp/spam"	# à vérifier
dossier_hams = "./spam/baseapp/ham"

fichiersspams = os.listdir(dossier_spams)
fichiershams = os.listdir(dossier_hams)

mSpam = len(fichiersspams)
mHam = len(fichiershams)

# Chargement du dictionnaire:
dictionnaire = charge_dico("./spam/dictionnaire1000en.txt")
print(dictionnaire)

# Apprentissage des bspam et bham:
print("apprentissage de bspam...")
bspam = apprendBinomial(dossier_spams, fichiersspams, dictionnaire)
print("apprentissage de bham...")
bham = apprendBinomial(dossier_hams, fichiershams, dictionnaire)

# Calcul des probabilités a priori Pspam et Pham:
# Pspam = 
# Pham = 


# Calcul des erreurs avec la fonction test():


