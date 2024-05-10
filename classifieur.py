import numpy as np
import os
import re
import pickle



def lireMail(fichier, dictionnaire):
    with open(fichier, "r", encoding="ascii", errors="surrogateescape") as f:
        contenu = f.read().lower()
        mots = re.split(r'\W+', contenu)
    return [mot in mots for mot in dictionnaire]

def charge_dico(fichier):

    with open(fichier, "r") as f:
        mots = [ligne.strip().lower() for ligne in f if len(ligne.strip()) >= 3]
    print("Chargé " + str(len(mots)) + " mots dans le dictionnaire")

    return mots

def apprendBinomial(dossier, dictionnaire):
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

def prediction(x, classifieur):

    
    proba_spam = np.log(classifieur['Pspam'])
    proba_ham = np.log(classifieur['Pham'])

    for i, val in enumerate(x):
        if val:
            proba_spam += np.log(classifieur['bspam'][i])
            proba_ham += np.log(classifieur['bham'][i])
        else:
            proba_spam += np.log(1 - classifieur['bspam'][i])
            proba_ham += np.log(1 - classifieur['bham'][i])

    return proba_spam > proba_ham

def testClassifieur(dossier, isSpam, classifieur, dictionnaire):
    fichiers = os.listdir(dossier)
    erreurs = 0
    total = len(fichiers)

    for fichier in fichiers:
        chemin_fichier = os.path.join(dossier, fichier)
        vecteur = lireMail(chemin_fichier, dictionnaire)
        predit_spam = prediction(vecteur, classifieur)
        if predit_spam != isSpam:
            erreurs += 1
            print(f"*** Erreur *** {'SPAM' if isSpam else 'HAM'} {chemin_fichier} identifié incorrectement")
    taux_erreur = erreurs / total
    return taux_erreur

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

# Stocker les paramètres dans un classifieur structuré
classifieur = {
    'Pspam': Pspam,
    'Pham': Pham,
    'bspam': bspam,
    'bham': bham
}

# Sauvegarder le classifieur avec pickle
with open('classifieur.pkl', 'wb') as f:
    pickle.dump(classifieur, f)

# Charger le classifieur avec pickle
with open('classifieur.pkl', 'rb') as f:
    classifieur = pickle.load(f)

# Test du classifieur
taux_erreur_spam = testClassifieur(os.path.join(dossier_test, 'spam'), True, classifieur, dictionnaire)
taux_erreur_ham = testClassifieur(os.path.join(dossier_test, 'ham'), False, classifieur, dictionnaire)
print(f"Taux d'erreur sur les spams: {taux_erreur_spam * 100:.2f}%")
print(f"Taux d'erreur sur les hams: {taux_erreur_ham * 100:.2f}%")
